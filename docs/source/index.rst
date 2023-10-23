=======================================
resfo: Low level IO for res files
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

   pip install resfo


Using the library
-----------------

.. testsetup::

    >>> import resfo
    >>>
    >>> resfo.write(
    ...     "my_grid.egrid",
    ...     [
    ...         ("FILEHEAD", []),
    ...         ("GRIDHEAD", []),
    ...         ("COORD", []),
    ...         ("ZCORN", []),
    ...         ("ACTNUM", []),
    ...         ("MAPAXES", []),
    ...     ],
    ...     fileformat=resfo.Format.FORMATTED,
    ... )

>>> import resfo
>>> for kw, arr in resfo.read("my_grid.egrid"):
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
