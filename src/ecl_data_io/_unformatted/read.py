import io

import ecl_data_io.types as ecl_io_types
import numpy as np
from ecl_data_io._unformatted.common import bytes_in_array, group_len, item_size
from ecl_data_io.array_entry import EclArray
from ecl_data_io.errors import EclParsingError


class UnformattedEclArray(EclArray):
    """
    An array entry in a unformatted ecl file.
    """

    def read_keyword(self):
        """
        Read the keyword from the unformatted ecl file.
        :returns: The keyword as a 8 character string.
        """
        if self._keyword is None:
            self._read()
        return self._keyword.decode("ascii")

    def read_array(self):
        """
        Read the array from the unformatted ecl file.
        :returns: numpy array of values.
        """
        if self._data_start is None:
            self._read()

        self.stream.seek(self._data_start)
        g_len = group_len(self.type)
        np_type = ecl_io_types.to_np_type(self._type)
        array = np.zeros(shape=(self._length,), dtype=np_type)
        to_read = self._length
        type_len = item_size(self._type)
        have_read = 0
        while to_read > 0:
            read_now = min(g_len, to_read)
            to_read -= read_now
            bytes_to_read = type_len * read_now
            self._read_record_marker(bytes_to_read)
            group_array = np.frombuffer(
                self.stream.read(bytes_to_read), dtype=np_type, count=read_now
            )
            array[have_read : have_read + read_now] = group_array
            have_read += read_now
            self._read_record_marker(bytes_to_read)

        if self._type == b"LOGI":
            array = array.astype(np.bool_)

        return array

    def _read_record_marker(self, expected_value):
        """
        Read 4 bytes and check that it matches the
        expected fortan header/footer
        """
        value = int.from_bytes(self.stream.read(4), byteorder="big", signed=True)
        if value != expected_value:
            raise EclParsingError(
                f"Unexpected size of record {value} ({value.to_bytes(4, byteorder='big', signed=True)})"
            )

    def _read_keyword(self):
        """
        With stream.peek() at the start of the keyword, reads
        it into self._keyword
        """
        self._keyword = self.stream.read(8)
        if not self._keyword or len(self._keyword) < 8:
            raise EclParsingError("Reached end-of-file while reading keyword")

    def _read_type(self):
        """
        With stream.peek() at the start of the type string, reads
        it into self._type
        """
        self._type = self.stream.read(4)
        if not self._type or len(self._type) < 4:
            raise EclParsingError("Reached end-of-file while reading type")

    def _read_length(self):
        """
        With stream.peek() at the start of the length, reads it and returns it.
        """
        length_bytes = self.stream.read(4)
        if not length_bytes or len(length_bytes) < 4:
            raise EclParsingError("Reached end-of-file while reading length")

        return int.from_bytes(length_bytes, byteorder="big", signed=True)

    def _read(self):
        """
        See ecl_data_io.array_entry.EclArray._read()
        """
        self.stream.seek(self.start)
        start_marker = self.stream.read(4)
        if not start_marker:
            self._is_eof = True
            return
        start_marker_value = int.from_bytes(start_marker, byteorder="big", signed=True)
        if start_marker_value != 16:
            raise EclParsingError(
                f"Unexpected size of record {start_marker_value} ({start_marker})"
            )
        self._read_keyword()
        self._length = self._read_length()
        self._read_type()
        self._read_record_marker(16)
        if self._type == b"X231":
            self._read_record_marker(16)
            self._length *= -(2 ** 31)
            previous_keyword = self._keyword
            self._read_keyword()
            if previous_keyword != self._keyword:
                raise EclParsingError(
                    "x231 type record was not followed "
                    f"by record with same keyword, found {self._keyword}"
                    f" expected {previous_keyword}"
                )
            self._length += self._read_length()
            self._read_type()
            self._read_record_marker(16)

        type_len = item_size(self._type)
        if self._length == 0:
            type_len = 0
        if type_len is None:
            raise EclParsingError(f"Unexpected item type {self._type}")
        if type_len <= 0 and self._length != 0:
            raise EclParsingError(
                f"Found keyword of type {self._type} which"
                f"has item length {type_len} which requires 0 number of"
                f"elements, but found {self._length} amount of elements."
            )
        bytes_to_skip = bytes_in_array(self._length, self.type)

        self._data_start = self.stream.tell()
        self.stream.seek(bytes_to_skip, io.SEEK_CUR)
