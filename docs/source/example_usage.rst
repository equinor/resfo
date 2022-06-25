.. _example-usage:

Example Usage
=============
The basic usage of ecl_data_io is to use the :meth:`ecl_data_io.read`
and :meth:`ecl_data_io.write` functions:


read
----

The read function will open a given file and give you a list of tuples
of the keywords and arrays.

>>> import ecl_data_io as eclio
>>> for kw, arr in eclio.read("my_grid.egrid"):
...     print(kw)
"FILEHEAD"
"GRIDHEAD"
"COORD"
"ZCORN"
"ACTNUM"
"MAPAXES"

write
-----

The :meth:`ecl_data_io.write` function will write such files
from lists of keywords, array tuples:

>>> import ecl_data_io as eclio
>>> eclio.write("my_grid.egrid", ["FILEHEAD": [...], "GRIDHEAD": [10,10,10]])

The default format is is binary (unformatted), but it is possible to
read and write ascii (formatted) aswell:


>>> import ecl_data_io as eclio
>>> eclio.write(
>>>     "my_grid.egrid",
>>>     {"FILEHEAD": [...], "GRIDHEAD": [10,10,10]},
>>>     fileformat=eclio.Format.FORMATTED
>>> )

lazy reading
------------

It is possible to read through the file without loading all arrays into
memory, ie. lazily:

import ecl_data_io as eclio

>>> for item in eclio.lazy_read("my_grid.egrid"):
>>>     print(item.read_keyword())
"FILEHEAD"
"GRIDHEAD"
"COORD"
"ZCORN"
"ACTNUM"
"MAPAXES"


Note that :meth:`ecl_data_io.lazy_read` in the above example is a generator of array
entries and the file will be closed once the generator is finished. Therefore,
care will have to be taken in when arrays/keywords are read from the entries.
For better control, one can pass the opened file:

>>> import ecl_data_io as eclio
>>>
>>> with open("my_grid.egrid", "rb") as f:
...     generator = eclio.lazy_read("my_grid.egrid")
...     item = next(generator)
...     print(item.read_keyword())

"FILEHEAD"

Writing MESS
------------

The special MESS types keyword can be written as follows:


>>> from ecl_data_io.types import MESS
>>> from ecl_data_io import write, MESS
>>> write("output.EGRID", [("MESSHEAD", MESS)])

array types
-----------

Generally, the array will translate the given python array to the
expected type of array in ecl. However, for better control a numpy
array can be passed with an explicit dtype for finer control. The
numpy dtypes are mapped to ecl file types as follows:

* INTE to `numpy.int32`
* REAL to `numpy.float32`
* DOUB to `numpy.float64`
* LOGI to `bool`
* CHAR to `string` (or `numpy.dtype("|S8")`)
* C0XX to `numpy.dtype("|SXX")`
