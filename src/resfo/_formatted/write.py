import numpy as np
import resfo.types as res_types
from resfo.errors import ResfoWriteError


def write_str_list(stream, str_list):
    """
    Writes the given list of strings to the res file.
    The strings will have the length of the longest string,
    left-padded with space and enclosed by single-quotes.
    """
    if len(str_list) == 0:
        return
    max_len = max(len(s) for s in str_list)
    str_list = [s.decode("ascii") if not isinstance(s, str) else s for s in str_list]

    for i, string in enumerate(str_list):
        if i % 7 == 0:
            stream.write("\n")
        stream.write(f" '{string.ljust(max_len)}'")


def write_np_array(stream, array, res_type):
    """
    Writes the given numpy array to the stream as
    the given res_type.
    :param stream: stream to write to.
    :param array: Numpy array.
    :param res_type: The res type to use for the array, see
        resfo.types.
    """
    if res_type == b"LOGI":
        for i, ele in enumerate(array):
            if i % 25 == 0:
                stream.write("\n")
            if ele:
                stream.write("  T")
            else:
                stream.write("  F")
    elif res_type == b"REAL":
        for i, ele in enumerate(array):
            if i % 4 == 0:
                stream.write("\n")
            stream.write(" {:>16.8E}".format(ele))
    elif res_type == b"DOUB":
        for i, ele in enumerate(array):
            if i % 3 == 0:
                stream.write("\n")
            stream.write(" {:>22.14E}".format(ele).replace("E", "D"))
    elif res_type == b"INTE":
        for i, ele in enumerate(array):
            if i % 6 == 0:
                stream.write("\n")
            stream.write(" {:>11d}".format(ele))


def write_entry(stream, keyword, array_like):
    """
    Write the given array/keyword entry to the
    stream in the formatted res file format.
    :param stream: text-mode stream to write to.
    :param keyword: 8-character string to use for keyword.
    :param array_like: Array of values to write.
    """
    if "'" in keyword:
        raise ResfoWriteError('keywords in formatted files cannot contain "\'"')
    array = np.asarray(array_like)
    try:
        res_type = res_types.from_np_dtype(array)
    except ValueError as e:
        raise ResfoWriteError(f"{e}") from e
    if res_type == b"MESS":
        stream.write(
            f" '{keyword.ljust(8)}' {' {:>10d}'.format(0)} '{res_type.decode('ascii').ljust(4)}'"
        )
    else:
        stream.write(
            f" '{keyword.ljust(8)}' {' {:>10d}'.format(len(array))} '{res_type.decode('ascii').ljust(4)}'"
        )

    if np.issubdtype(array.dtype, np.str_) or array.dtype.char == "S":
        write_str_list(stream, array.tolist())
    else:
        write_np_array(stream, array, res_type)


def formatted_write(stream, keyworded_arrays):
    """
    Writes the list of data entries to the stream as
    formatted res.
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
