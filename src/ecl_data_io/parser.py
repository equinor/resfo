import io
import warnings


class UnexpectedKeywordException(Exception):
    pass


class Parser:
    def __init__(
        self, text_stream, subparsers, strict=True, comment_token="--", max_length=8
    ):
        self.subparsers = {sb.keyword: sb for sb in subparsers}
        self.strict = strict
        self.text_stream = text_stream
        self.col_start = 0
        self.col_end = 132
        self.comment_token = comment_token
        self.max_length = max_length

        for sb in subparsers:
            if max_length and len(sb.keyword) > max_length:
                warnings.warn("Subparser keyword {sb.keyword} exceeds max length!")

    def line_iterator(self):
        for line in self.text_stream:
            new_line = self.preprocess_line(line)
            if new_line:
                yield new_line

    def preprocess_line(self, line):
        dropped_col = line[self.col_start : self.col_end]
        if self.comment_token in dropped_col:
            dropped_comment = dropped_col[dropped_col.index(self.comment_token) :]
        else:
            dropped_comment = dropped_col
        return dropped_comment

    def __iter__(self):
        lines = self.line_iterator()
        did_warn = False
        while True:
            try:
                line = next(lines)
            except StopIteration:
                return

            if self.max_length:
                keyword = line[0 : min(len(line), self.max_length)].rstrip()
            else:
                keyword = line.split()[0]
            subparser = self.subparsers.get(keyword, None)
            if subparser is None:
                if self.strict:
                    raise UnexpectedKeywordException(f"Unexpected keyword {line}")
                elif not did_warn:
                    warnings.warn(f"Unexpected keyword {line}")
                    did_warn = True
                    continue
            did_warn = False
            yield from subparser.parse(self, lines)

    def parse_str(self, string):
        yield from iter(Parser(io.StringIO(string), self.subparsers.values()))
