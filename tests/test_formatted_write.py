import io

import ecl_data_io._formatted.write as ecl_io_fwrite


def test_write_str_list():
    buf = io.StringIO()
    ecl_io_fwrite.write_str_list(buf, ["a", "bb"])

    assert buf.getvalue() == " 'a ' 'bb'"
