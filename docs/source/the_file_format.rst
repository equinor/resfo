The File Format
===============

The file format used by several oil reservoir simulators originate
in fortrans `WRITE` and `READ` functions which had two modes, formatted
or unformatted. Formatted would produce ASCII and unformatted produced binary.

General layout
--------------

The file consists of a series of records holding information about a named array.
Each record has the following fields (in the order they appear):

1. The keyword (the arrays name)
2. The length of the array
3. The type of the array
4. The data of the array (the elements)

The keyword is a ascii string of 8 characters, the length a 32bit number, and
the type one of the following 4 character strings:

* INTE
* REAL
* LOGI
* CHAR
* C0XX (where XX is a number between 01 and 99)
* MESS
* X231

.. _formatted-format:

Formatted
---------

The formatted res file format is very similar to the the unformatted
files, except ascii. The layout is as follows

* keyword
* length
* type
* values

Both the keyword and type is delimited by single quotes, and uses
padding:

'SWAT ' 3 'REAL'
 0.10500000E+00 0.10500000E+00 0.10500000E+00


Some, perhaps most, reservoir simulators that implement this format
are fussy about the whitespace, both between numbers and string literals
and padding inside string literals.


The keyword, length and type uses the following Fortran formatting specifyer::

    (1X, "'", A8, "'", 1X, I11, 1X, "'", A4, "'")

On the next line starts the elements of the array which have the following fortran
formatting specifiers, based on type:

* INTE: `6(1X, I11)`
* REAL: `4(1X, E16.8)`
* LOGI: `25(1X, L2)`
* DOUB: `3(1X, D22.14)`
* CHAR: `7(1X, "'", A8, "'")`
* COXX: `(1X, "'", AXX, "'")`


.. _unformatted-format:

Unformatted
-----------

The unformatted res file format is a binary format based on the fortran fwrite.

All numerical values are big-endian.

Generally, each array/keyword pair is layed out as follows:

* Fortran header
* keyword
* array length
* element type
* Fortran footer
* Fortran header
* grouped array elements
* Fortran footer

The exceptions to this layout is arrays of length > 2**31 which has an
additional header of type X231:

* Fortran header
* keyword
* array length // 2**31 * -1
* X231
* Fortran footer
* Fortran header
* keyword
* array length % 2**31
* element type
* Fortran footer
* Fortran header
* grouped array elements
* Fortran footer

The fortran header and footer is a 4 byte signed integer of the number
of bytes in the group. Since keywords are 4 charactes, array length
is a 32bit integer and the type is a 4 character string, the first header
and footer is both 8+4+4=16.

Each array has a max number of elements per group, 1000 for numerical values
and 105 for strings. Hence 1500 int elements will be layed out as follows:

* 16 (fortran header)
* KEYWORD1
* 1500 (as big endian 32bit integer)
* INTE
* 16 (fortran footer)
* 4000 (fortran header)
* first 1000 elements
* 4000 (fortran footer)
* 2000 (fortran header)
* last 500 elements
* 2000 (fortran footer)
