import io

import ecl_data_io._formatted.write as ecl_io_fwrite
import numpy as np


def test_write_str_list():
    buf = io.StringIO()
    ecl_io_fwrite.write_str_list(buf, ["a", "bb"])

    assert buf.getvalue() == "\n 'a ' 'bb'"


def test_write_str():
    buf = io.StringIO()
    ecl_io_fwrite.formatted_write(buf, [("ZGRP    ", ["12345678"] * 8)])

    assert (
        buf.getvalue()
        == """ 'ZGRP    '           8 'CHAR'
 '12345678' '12345678' '12345678' '12345678' '12345678' '12345678' '12345678'
 '12345678'\n"""
    )


def test_write_int():
    buf = io.StringIO()
    ecl_io_fwrite.formatted_write(
        buf, [("FILEHEAD", np.zeros(shape=(7,), dtype=np.int32))]
    )

    assert (
        buf.getvalue()
        == """ 'FILEHEAD'           7 'INTE'
           0           0           0           0           0           0
           0\n"""
    )


def test_write_logi():
    buf = io.StringIO()
    ecl_io_fwrite.formatted_write(
        buf, [("LOGIHEAD", np.zeros(shape=(26,), dtype=np.bool))]
    )

    assert (
        buf.getvalue()
        == """ 'LOGIHEAD'          26 'LOGI'
  F  F  F  F  F  F  F  F  F  F  F  F  F  F  F  F  F  F  F  F  F  F  F  F  F
  F\n"""
    )


def test_write_doub():
    buf = io.StringIO()
    ecl_io_fwrite.formatted_write(
        buf, [("DOUBHEAD", np.zeros(shape=(4,), dtype=np.float64))]
    )

    assert (
        buf.getvalue()
        == """ 'DOUBHEAD'           4 'DOUB'
   0.00000000000000D+00   0.00000000000000D+00   0.00000000000000D+00
   0.00000000000000D+00\n"""
    )
