ecl-data-io
===========
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![docs](https://readthedocs.org/projects/ecl-data-io/badge/?version=latest&style=plastic)](https://ecl-data-io.readthedocs.io/)

Parser for the ecl output format, such as found in files with
extensions .UNRST, .EGRID, .INIT, etc. and also the corresponding
ascii files with extension .FUNRST, .FEGRID, .FINIT, etc.


Installation
============

ecl-data-io can be installed with pip:

```bash
pip install ecl-data-io
```

Getting started
===============

Ecl output files consist of a sequence of named arrays. ecl-data-io does not
interpret the names, but simply give you a tuple of the name and a numpy array
with the read function:

```
import ecl_data_io as eclio

for kw, arr in eclio.read("my_grid.egrid"):
    print(kw)

>>> "FILEHEAD"
>>> "GRIDHEAD"
>>> "COORD"
>>> "ZCORN"
>>> "ACTNUM"
>>> "MAPAXES"
```

For more information, see [the docs](http://ecl-data-io.rtfd.io).
