def group_len(type_keyword):
    """
    The length of element groups in unformatted arrays.
    """
    if type_keyword[0:1] == b"C":
        return 105
    else:
        return 1000


# The number of bytes for each
# ecl type except C0nn which varies
static_item_sizes = {
    b"INTE": 4,
    b"REAL": 4,
    b"LOGI": 4,
    b"DOUB": 8,
    b"CHAR": 8,
    b"MESS": 0,
    b"X231": 0,
}


def item_size(type_keyword):
    """
    :returns: The number of bytes for each element in an
        ecl array of the given ecl type.
    """
    if type_keyword[0:2] == b"C0":
        return int(type_keyword[2:4].decode("ascii"))
    return static_item_sizes.get(type_keyword, None)


def bytes_in_array(array_length, item_type):
    """
    :param array_length: Number of items in the array
    :param item_type: Type of items in the array
    :returns: Number of bytes used to store an array of
        given type and length
    """
    g_len = group_len(item_type)
    full_groups = array_length // g_len

    if array_length % g_len:
        return (full_groups + 1) * 8 + array_length * item_size(item_type)
    else:
        return full_groups * 8 + array_length * item_size(item_type)
