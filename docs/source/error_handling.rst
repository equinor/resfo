Error Handling
==============

Reading of res files will throw :py:class:`resfo.ResfoParsingError`
when the given file does not contain valid res data:

.. doctest::

    >>> from resfo import read, write, ResfoParsingError, ResfoWriteError
    >>> from io import StringIO
    >>>
    >>> file_contents = StringIO("Not valid res content")
    >>> try:
    ...   read(file_contents)
    ... except ResfoParsingError as e:
    ...   print(e)
    Expected "'" before keyword, got N at 1

Similarly, write will produce :py:class:`resfo.ResfoWriteError`
when the given data is not suitable for writing.

.. doctest::

    >>> try:
    ...   write("my_file.egrid", [("FILEHEAD", ["a"*100])])
    ... except ResfoWriteError as e:
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
