"""
The types of elements in the eclipse output files are
INTE for 32-bit integers, REAL for 32-bit floats,
LOGI for 32-bit fortran logicals, DOUB for 64-bit floats,
CHAR for 8 byte ascii strings, and C0nn for nn byte ascii strings.

All numerical types are big endian.

Additionally there are two types that signal something other than
what is contained in the arrays. X231 means that the following array
has more than 2**31 elements so the length is split into two headers.

The other is MESS type which signals a 0 length array, so the type
of elements is irrelevant.


A ecl type is represented by a byte string of ascii characters
having one of the above mentioned keywords.

ecl_data_io converts ecl types to corresponding numpy dtypes
and back. Some numpy dtypes will give a loss of precision and
that results in a warning.

"""
import warnings

import numpy as np

# np dtype for ecl types with fixed width
static_dtypes = {
    b"INTE": np.dtype(np.int32).newbyteorder(">"),
    b"REAL": np.dtype(np.float32).newbyteorder(">"),
    b"LOGI": np.dtype(np.int32).newbyteorder(">"),
    b"DOUB": np.dtype(np.float64).newbyteorder(">"),
    b"CHAR": np.dtype("|S8"),
}


def to_np_type(type_keyword):
    """
    :param type_keyword: A bytestring of a ecl type.
    :returns: A np dtype corresponding to the given
        ecl type.
    """
    if type_keyword[0:2] == b"C0":
        return np.dtype("|S" + type_keyword[2:4].decode("ascii"))
    return static_dtypes.get(type_keyword, None)


def from_np_dtype(array):
    """
    :param array: A numpy array
    :returns: The corresponding ecl type for the
        given numpy array's dtype.
    """
    dtype = array.dtype
    if dtype in [np.dtype(np.int32), np.dtype(np.int32).newbyteorder(">")]:
        return b"INTE"
    if dtype in [np.dtype(np.int64), np.dtype(np.int64).newbyteorder(">")]:
        warnings.warn("downcasting numpy int64 to int32 for ecl file.")
        return b"INTE"
    if dtype in [np.dtype(np.float32), np.dtype(np.float32).newbyteorder(">")]:
        return b"REAL"
    if dtype in [np.dtype(np.float64), np.dtype(np.float64).newbyteorder(">")]:
        return b"DOUB"
    if dtype == np.dtype(np.bool_):
        return b"LOGI"
    if dtype == np.dtype("|S8"):
        return b"CHAR"
    if dtype == np.dtype("|S") or dtype == np.dtype("U"):
        max_len = max(len(s) for s in array)
        if max_len > 99:
            raise ValueError("ecl filetype only supports string length up to 99")
        if max_len == 8:
            return b"CHAR"
        return b"C0" + str(max_len).zfill(2).encode("ascii")
    if dtype.char == "U" and 0 < dtype.itemsize < 4 * 99:
        size = dtype.itemsize // 4
        if size == 8:
            return b"CHAR"
        return b"C0" + str(size).zfill(2).encode("ascii")
    if dtype.char == "S" and 0 < dtype.itemsize < 99:
        size = dtype.itemsize
        if size == 8:
            return b"CHAR"
        return b"C0" + str(size).zfill(2).encode("ascii")
    raise ValueError(f"Could not convert numpy type {dtype} in {array}")


def is_valid_type(type_str):
    """
    :returns: Whether the given byte string is a valid ecl type.
    """
    if type_str in static_dtypes.keys():
        return True
    if type_str in [b"X231", b"MESS"]:
        return True
    return type_str[0:2] == b"C0" and all(48 <= kw <= 57 for kw in type_str[2:4])


def is_character_type(type_str):
    """
    :returns: Whether the given byte string as ascii is
        a string ecl type, ie. b"CHAR" or b"C016".
    """
    return type_str and type_str[0:1] == b"C"
