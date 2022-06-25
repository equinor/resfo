=======================================
ecl-data-io: Low level IO for ecl files
=======================================

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Contents:

   example_usage
   the_file_format
   developer_guide
   api_doc



Quick Start Guide
=================

.. code-block:: console

   pip install ecl_data_io


Using the library
-----------------

>>> import ecl_data_io as eclio
>>> for kw, arr in eclio.read("my_grid.egrid"):
...     print(kw)
"FILEHEAD"
"GRIDHEAD"
"COORD"
"ZCORN"
"ACTNUM"
"MAPAXES"


For more see :ref:`example-usage`.



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
