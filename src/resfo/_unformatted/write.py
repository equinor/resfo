import warnings

import numpy as np
import resfo.types as res_types
from resfo._unformatted.common import group_len, item_size
from resfo.errors import ResfoWriteError


def write_array_header(stream, kw_str, type_str, size):
    if len(kw_str) != 8:
        raise ResfoWriteError("keywords must have length exactly size 8")
    if not res_types.is_valid_type(type_str):
        raise ResfoWriteError(f"Not a valid res type: {type_str}")

    if size > 2**31:
        write_array_header(stream, kw_str, b"X231", -(size // (2**31)))
        size %= 2**31

    stream.write((16).to_bytes(4, byteorder="big", signed=True))
    stream.write(kw_str.encode("ascii"))
    stream.write(size.to_bytes(4, byteorder="big", signed=True))
    stream.write(type_str)
    stream.write((16).to_bytes(4, byteorder="big", signed=True))


def cast_array_to_res(arr):
    if arr.dtype.type in [np.int32, np.float32, np.float64]:
        return arr.astype(arr.dtype.newbyteorder(">"))
    if np.issubdtype(arr.dtype, np.bool_):
        return -arr.astype(">i4")
    elif np.issubdtype(arr.dtype, np.integer):
        result_dtype = ">i4"
    elif np.issubdtype(arr.dtype, np.floating):
        result_dtype = ">f8"
    else:
        raise ValueError(f"Cannot cast {arr.dtype} to a res type")

    warnings.warn(f"casting array dtype {arr.dtype} to {result_dtype}")
    return arr.astype(result_dtype)


def write_np_array(stream, arr):
    arr = np.asarray(arr)
    res_type = res_types.from_np_dtype(arr)
    if res_type == b"C008":
        raise ValueError()
    g_len = group_len(res_type)
    to_write = len(arr)
    type_len = item_size(res_type)
    have_written = 0
    arr = cast_array_to_res(arr)
    while to_write > 0:
        write_now = min(g_len, to_write)
        to_write -= write_now
        bytes_to_write = type_len * write_now
        stream.write(bytes_to_write.to_bytes(4, byteorder="big", signed=True))
        stream.write(arr[have_written : have_written + write_now].tobytes())
        have_written += write_now
        stream.write(bytes_to_write.to_bytes(4, byteorder="big", signed=True))


def write_str_list(stream, str_list, res_type):
    str_size = item_size(res_type)
    if len(str_list) == 0:
        return
    max_len = max(len(s) for s in str_list)
    if max_len > 99:
        raise ResfoWriteError("Res files does not support strings of length > 99")
    if max_len > str_size:
        raise ResfoWriteError(
            f"Inconsistent type size, have {str_size} type but longest string is {max_len}"
        )
    str_list = [s.ljust(str_size) for s in str_list]
    try:
        byte_str_list = [
            s.encode("ascii") if isinstance(s, str) else s for s in str_list
        ]
    except UnicodeEncodeError as e:
        raise ResfoWriteError(
            "Cannot write non-ascii strings to unformatted res files"
        ) from e

    g_len = group_len(res_type)
    to_write = len(byte_str_list)
    type_len = item_size(res_type)
    have_written = 0
    while to_write > 0:
        write_now = min(g_len, to_write)
        to_write -= write_now
        bytes_to_write = type_len * write_now
        stream.write(bytes_to_write.to_bytes(4, byteorder="big", signed=True))
        for i in range(have_written, have_written + write_now):
            stream.write(byte_str_list[i])
        have_written += write_now
        stream.write(bytes_to_write.to_bytes(4, byteorder="big", signed=True))


def write_array_like(stream, keyword, array_like):
    array = np.asarray(array_like)
    try:
        res_type = res_types.from_np_dtype(array)
    except ValueError as e:
        raise ResfoWriteError(f"{e}") from e
    if res_type == b"MESS":
        write_array_header(stream, keyword, res_type, 0)
        array = np.array([])
    else:
        write_array_header(stream, keyword, res_type, len(array))
    if np.issubdtype(array.dtype, np.str_) or array.dtype.char == "S":
        write_str_list(stream, array.tolist(), res_type)
    else:
        write_np_array(stream, array)


def unformatted_write(stream, keyworded_arrays):
    iterator = keyworded_arrays
    if hasattr(keyworded_arrays, "items"):
        iterator = keyworded_arrays.items()
    for keyword, array in iterator:
        write_array_like(stream, keyword, array)
