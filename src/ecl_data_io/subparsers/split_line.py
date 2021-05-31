def split_line(line):
    value = ""
    for char in line:
        if value.startswith("'"):
            # a string literal
            if char == "'":
                yield value + char
            else:
                value += char
        elif value and value[-1] == "-" and char == "-":
            # a comment
            value = value[0:-1]
            break
        elif char.isspace():
            # delimiting space
            if value:
                yield value
                value = ""
        else:
            value += char
    if value:
        yield value
