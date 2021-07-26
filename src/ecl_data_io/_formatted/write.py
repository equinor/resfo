import numpy as np

import ecl_data_io.types as ecl_types
from ecl_data_io.errors import EclWriteError


def write_str_list(stream, str_list):
    """
    Writes the given list of strings to the ecl file.
    The strings will have the length of the longest string,
    left-padded with space and enclosed by single-quotes.
    """
    if len(str_list) == 0:
        return
    max_len = max(len(s) for s in str_list)
    str_list = [s.decode("ascii") if not isinstance(s, str) else s for s in str_list]

    for i, string in enumerate(str_list):
        stream.write(f" '{string.ljust(max_len)}'")
        if i % 4 == 3:
            stream.write("\n")


def write_np_array(stream, array, ecl_type):
    """
    Writes the given numpy array to the stream as
    the given ecl_type.
    :param stream: stream to write to.
    :param array: Numpy array.
    :param ecl_type: The ecl type to use for the array, see
        ecl_data_io.types.
    """
    if ecl_type == b"LOGI":
        for i, ele in enumerate(array):
            if ele:
                stream.write(" T")
            else:
                stream.write(" F")
            if i % 4 == 3:
                stream.write("\n")
    elif ecl_type == b"REAL":
        for i, ele in enumerate(array):
            stream.write(" {:16.8E}".format(ele))
            if i % 4 == 3:
                stream.write("\n")
    elif ecl_type == b"DOUB":
        for i, ele in enumerate(array):
            stream.write(" {:22.14E}".format(ele))
            if i % 4 == 3:
                stream.write("\n")
    elif ecl_type == b"INTE":
        for i, ele in enumerate(array):
            stream.write(" {:10d}".format(ele))
            if i % 4 == 3:
                stream.write("\n")


def write_entry(stream, keyword, array_like):
    """
    Write the given array/keyword entry to the
    stream in the formatted ecl file format.
    :param stream: text-mode stream to write to.
    :param keyword: 8-character string to use for keyword.
    :param array_like: Array of values to write.
    """
    array = np.asarray(array_like)
    ecl_type = ecl_types.from_np_dtype(array)
    stream.write(
        f"'{keyword.ljust(8)}' {len(array)} '{ecl_type.decode('ascii').ljust(4)}'\n"
    )

    if np.issubdtype(array.dtype, np.str_) or array.dtype.char == "S":
        write_str_list(stream, array.tolist())
    else:
        write_np_array(stream, array, ecl_type)


def formatted_write(stream, keyworded_arrays):
    """
    Writes the list of data entries to the stream as
    formatted ecl.
    :param stream: File handle in text mode.
    :param keyworded_arrays: Either iterable or list of (kw, array)
        tuples for entries to be written to the file. Also takes dictionary
        of keyword: array pairs.
    """
    iterator = keyworded_arrays
    if hasattr(keyworded_arrays, "items"):
        iterator = keyworded_arrays.items()
    for keyword, array in iterator:
        write_entry(stream, keyword, array)
        stream.write("\n")
