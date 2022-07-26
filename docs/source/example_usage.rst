.. _example-usage:

Example Usage
=============
The basic usage of ecl_data_io is to use the :meth:`ecl_data_io.read`
and :meth:`ecl_data_io.write` functions:


read
----

The read function will open a given file and give you a list of tuples
of the keywords and arrays.

.. testsetup::

    >>> import ecl_data_io as eclio
    >>>
    >>> eclio.write(
    ...     "my_grid.egrid",
    ...     [
    ...         ("FILEHEAD", []),
    ...         ("GRIDHEAD", []),
    ...         ("COORD", []),
    ...         ("ZCORN", []),
    ...         ("ACTNUM", []),
    ...         ("MAPAXES", []),
    ...     ],
    ...     fileformat=eclio.Format.FORMATTED,
    ... )

>>> import ecl_data_io as eclio
>>> for kw, arr in eclio.read("my_grid.egrid"):
...     print(kw.strip())
FILEHEAD
GRIDHEAD
COORD
ZCORN
ACTNUM
MAPAXES

write
-----

The :meth:`ecl_data_io.write` function will write such files
from lists of keywords, array tuples:

>>> eclio.write("my_grid.egrid", [("FILEHEAD", [1]), ("GRIDHEAD", [10,10,10])])

The default format is is binary (unformatted), but it is possible to
read and write ascii (formatted) aswell:


>>> eclio.write(
...     "my_grid.fegrid",
...     {"FILEHEAD": [1], "GRIDHEAD": [10,10,10]},
...     fileformat=eclio.Format.FORMATTED
... )

lazy reading
------------

It is possible to read through the file without loading all arrays into
memory, ie. lazily:

>>> for item in eclio.lazy_read("my_grid.fegrid"):
...     print(item.read_keyword())
FILEHEAD
GRIDHEAD


Note that :meth:`ecl_data_io.lazy_read` in the above example is a generator of array
entries and the file will be closed once the generator is finished. Therefore,
care will have to be taken in when arrays/keywords are read from the entries.
For better control, one can pass the opened file:

>>> import ecl_data_io as eclio
>>>
>>> with open("my_grid.egrid", "rb") as f:
...     generator = eclio.lazy_read(f)
...     item = next(generator)
...     print(item.read_keyword())
FILEHEAD

Writing MESS
------------

The special MESS types keyword can be written as follows:


>>> eclio.write("output.EGRID", [("MESSHEAD", eclio.MESS)])

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

Updating
--------

It is possible to do an in-place update of an array in an existing
file, by passing a stream opened for both read and write. The array
cannot change type or size.

Say you want to update the first keyword name `"OLD_NAME"`, change the array
to `new_array` and the name to `NEW_NAME`, then that can be done
with the following:

>>> new_array = [2]
>>>
>>> with open("my_grid.egrid", "br+") as f: # Open with read and write
...     for entry in eclio.lazy_read(f):
...         if entry.read_keyword() == "FILEHEAD":
...             entry.update(keyword="FILEHEAD", array=new_array)
...             break
