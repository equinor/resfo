import io
from abc import ABC, abstractmethod

import numpy as np

import ecl_data_io.types as ecl_io_types
from ecl_data_io._unformatted.common import group_len, item_size
from ecl_data_io.errors import EclParsingError


class EclArray(ABC):
    """
    An array entry in a ecl file.
    """

    def __init__(self, stream):
        """
        :param stream: The opened ecl file with stream.peek() at
            the start of the ecl array.
        """
        self.start = stream.tell()
        self.stream = stream

        self._keyword = None
        self._length = None
        self._type = None
        self._data_start = None

        self._is_eof = False

    @property
    def is_eof(self):
        """
        Whether the position of the array is actually
        at the end of the file, in which case its keyword
        and array is None.
        """
        if self._keyword is None:
            self._read()
        return self._is_eof

    @abstractmethod
    def read_keyword(self):
        """
        Read the keyword from the ecl file.
        :returns: The keyword as a 8 character string.
        """
        pass

    @abstractmethod
    def read_array(self):
        """
        Read the array from the unformatted ecl file.
        :returns: numpy array of values.
        """
        pass

    @property
    def type(self):
        """
        The type given in the header of the array
        """
        if self._type is None:
            self._read()
        return self._type

    @property
    def length(self):
        """
        The length given in the header of the array
        """
        if self._length is None:
            self._read()
        return self._length

    @abstractmethod
    def _read(self):
        """
        Reads the array entry. Guarantees that after, either entry.is_eof() and
        the stream.peek() is at the end of the file or stream.peek() will be at
        the start of the next record.
        """
        pass

    @classmethod
    def parse(cls, stream):
        """
        Parse an ecl file from the given opened file handle.

        Is a generator of EclArrays
        """
        record = cls(stream)

        record._read()

        while not record._is_eof:
            new_record = cls(stream)
            yield record
            new_record._read()
            record = new_record
