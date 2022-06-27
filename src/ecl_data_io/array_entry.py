from abc import ABC, abstractmethod


class EclArray(ABC):
    """
    An array entry in a ecl file.

    This class is not ment to be constructed directly, but rather
    generated e.g. :py:meth:`ecl_data_io.lazy_read`.
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

    def read_keyword(self):
        """
        Read the keyword from the ecl file.

        :returns: The keyword as a 8 character string.
        """
        if self._keyword is None:
            self._read()
        return self._keyword

    def read_length(self):
        """
        Read the length from the ecl file.

        :returns: The length of the array in number of entries.
        """
        if self._length is None:
            self._read()
        return self._length

    @abstractmethod
    def read_array(self):
        """
        Read the array from the unformatted ecl file.

        :returns: numpy array of values.
        """
        pass

    def read_type(self):
        """
        The type given in the header of the array
        """
        if self._type is None:
            self._read()
        return self._type

    @abstractmethod
    def update(self, *, keyword=None, array=None):
        """
        Updates the entry with the given new data.

        :param new_keyword: The new keyword, must be 8 characters, defaults to no change.
        :param new_array: The new array, must be of same type and size
            as existing array, defaults to no change.

        :raises ValueError: If array does not have the same type or length as
            existing array.
        :raises io.UnsupportedOperation: If the underlying stream has been opened
            with the wrong mode (file must be opened with "r+" in order to correctly update)
        """
        pass

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
