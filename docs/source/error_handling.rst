Error Handling
==============

Reading of ecl files will throw :py:class:`ecl_data_io.EclParsingError`
when the given file does not contain valid ecl data:

.. doctest::

    >>> from ecl_data_io import read, write, EclParsingError, EclWriteError
    >>> from io import StringIO
    >>>
    >>> file_contents = StringIO("Not valid ecl content")
    >>> try:
    ...   read(file_contents)
    ... except EclParsingError as e:
    ...   print(e)
    Expected "'" before keyword, got N at 1

Similarly, write will produce :py:class:`ecl_data_io.EclWriteError`
when the given data is not suitable for writing.

.. doctest::

    >>> try:
    ...   write("my_file.egrid", [("FILEHEAD", ["a"*100])])
    ... except EclWriteError as e:
    ...   print(e)
    Could not convert numpy type <U100...


For file and stream operations, the underlying exceptions from open(), read(), and
write() are passed through:

.. doctest::

    >>> try:
    ...   read("does_not_exist/my_file.egrid", [])
    ... except OSError as e:
    ...   print(e)
    [Errno 2] No such file or directory...
