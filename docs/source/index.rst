=======================================
ecl-data-io: Low level IO for ecl files
=======================================

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Contents:

   example_usage
   the_file_format
   error_handling
   developer_guide
   api_doc



Quick Start Guide
=================

.. code-block:: console

   pip install ecl_data_io


Using the library
-----------------

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


For more see :ref:`example-usage`.



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
