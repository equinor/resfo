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
    b"X231": None,
}


def item_size(type_keyword):
    """
    :returns: The number of bytes for each element in an
        ecl array of the given ecl type.
    """
    if type_keyword[0:2] == b"C0":
        return int(type_keyword[2:4].decode("ascii"))
    return static_item_sizes.get(type_keyword, None)
