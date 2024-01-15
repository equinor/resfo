resfo
===========
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![docs](https://readthedocs.org/projects/resfo/badge/?version=latest&style=plastic)](https://resfo.readthedocs.io/)

resfo (Reservoir simulator fortran output) is a parser for the output format
used by several reservoir simulators such as [opm
flow](https://github.com/OPM/opm-simulators), such as found in files with
extensions .UNRST, .EGRID, .INIT, etc. and also the corresponding ascii files
with extension .FUNRST, .FEGRID, .FINIT, etc.


Installation
============

resfo can be installed with pip:

```bash
pip install resfo
```

Getting started
===============

Reservoir simulator output files consist of a sequence of named arrays. resfo
does not interpret the names, but simply give you a tuple of the name and a
numpy array with the read function:

```
import resfo

for kw, arr in resfo.read("my_grid.egrid"):
    print(kw)

>>> "FILEHEAD"
>>> "GRIDHEAD"
>>> "COORD"
>>> "ZCORN"
>>> "ACTNUM"
>>> "MAPAXES"
```

For more information, see [the docs](http://resfo.rtfd.io).


How to contribute
=================

The easiest way to set up a nice development environment for resfo is to use tox (can be installed via `pip install tox` or
`sudo apt install tox` on ubuntu), then all testing and linting can be ran with

```bash
tox
```

You can also set up `pre-commit` to ensure style checks are done as you commit:

```bash
pip install pre-commit
pre-commit install
```
