import numpy as np

import resfo.types as res_types
from resfo.array_entry import ResArray
from resfo.errors import ResfoParsingError


def drop_while_space(stream):
    """
    Forwards the stream to the first non-space character.
    Assumes the stream is in text mode.
    """
    first_non_space = stream.tell()
    while stream.read(1).isspace():
        first_non_space = stream.tell()
    stream.seek(first_non_space)


class FormattedArray(ResArray):
    """
    An array entry in an formatted res file.
    """

    def __init__(self, stream):
        self.start = stream.tell()
        self.stream = stream

        self._keyword = None
        self._length = None
        self._type = None
        self._data_start = None
        self._array = None

        self._is_eof = False

    def read_array(self):
        if self._keyword is None:
            self._read()
        return self._read_array()

    def update(self, *, keyword=None, array=None):
        raise NotImplementedError("Update is not implemented for formatted files")

    def _read_logical(self):
        """
        Read one fortran logical ('T' or 'F') from
        the beginning of the stream and returns it.
        """
        drop_while_space(self.stream)
        current_char = self.stream.read(1)
        if current_char == "T":
            return True
        elif current_char == "F":
            return False
        else:
            raise ResfoParsingError(f"Could not parse logical value {current_char}")

    def _read_quote_separated(self):
        """
        Read one single-quote delimited string from the
        start of the stream, and returns it.
        """
        drop_while_space(self.stream)
        current_char = self.stream.read(1)
        if current_char != "'":
            raise ResfoParsingError(
                f'Expected "\'" before keyword, got {current_char} at {self.stream.tell()}'
            )
        word = ""

        current_char = self.stream.read(1)
        while current_char != "'":
            word += current_char
            current_char = self.stream.read(1)
            if not current_char:
                raise ResfoParsingError(
                    f"Reached end-of-file while reading keyword {word}"
                )

        return word

    def _read_number(self):
        """
        Read one number from the stream and returns it as a string.
        """
        drop_while_space(self.stream)
        word = ""

        current_char = self.stream.read(1)
        while current_char in "0123456789DE.+-":
            word += current_char
            current_char = self.stream.read(1)
            if not current_char:
                raise ResfoParsingError(
                    f"Reached end-of-file while reading number {word} at {self.stream.tell()}"
                )

        if not current_char.isspace() and current_char:
            raise ResfoParsingError(
                f"Expected space after number at {self.stream.tell()} got {current_char}"
            )

        if not word:
            raise ResfoParsingError(f"Could not read number at {self.stream.tell()}")

        return word.replace("D", "E")

    def _read_keyword(self):
        self._keyword = self._read_quote_separated()

    def _read_type(self):
        self._type = self._read_quote_separated().encode("ascii")

    def _read_length(self):
        drop_while_space(self.stream)
        self._length = np.fromfile(
            self.stream,
            sep=" ",
            count=1,
            dtype=np.int32,
        )[0]

    def _read_array(self):
        self.stream.seek(self._data_start)
        drop_while_space(self.stream)
        if self._type == b"MESS":
            return res_types.MESS
        if res_types.is_character_type(self._type):
            return np.array([self._read_quote_separated() for i in range(self._length)])
        elif self._type == b"LOGI":
            return np.array([self._read_logical() for i in range(self._length)])
        else:
            return np.array(
                [self._read_number() for i in range(self._length)],
                dtype=res_types.to_np_type(self._type),
            )

    def _read(self):
        """
        See resfo.array_entry.ResArray._read()
        """
        self.stream.seek(self.start)
        drop_while_space(self.stream)
        if not self.stream.read(1):
            self._is_eof = True
            return
        else:
            self.stream.seek(self.start)
        self._read_keyword()
        self._read_length()
        self._read_type()
        self._data_start = self.stream.tell()
        self._read_array()
