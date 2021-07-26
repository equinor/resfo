"""
The unformatted ecl file format is a binary format based on the fortran fwrite.

All numerical values are big-endian.

Generally, each array/keyword pair is layed out  as follows:

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


"""
