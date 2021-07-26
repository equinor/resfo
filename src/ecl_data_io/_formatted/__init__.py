"""
The formatted ecl file format is very similar to the the unformatted
files, except ascii. The layout is as follows

* keyword
* length
* type
* values

Both the keyword and type is delimited by single quotes:

    'KEYWORD ' 3 'INTE' 1 2 3

"""
