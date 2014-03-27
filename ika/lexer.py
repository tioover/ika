import re
from functools import reduce
from .const import token_patterns, remove_pattern

# compile patterns.
compile = lambda patterns: list(map(re.compile, patterns))
token_res = compile(token_patterns)
remove_re = re.compile(remove_pattern)


def token_gen(row):
    while row:
        # remove space and comment.
        remove_match = remove_re.match(row)
        if remove_match:
            row = row[remove_match.end():]
            continue

        for sre in token_res:
            match = sre.match(row)
            if match is not None:
                yield row[:match.end()]  # return matched token.
                row = row[match.end():]  # split row.
                break  # stop!

        if match is None:  # row is not "", and nothing matched.
            raise SyntaxError("Can't recognize token: %s" % row)


def lexer(string):
    def add(li, token):
        li.append(token)
        return li
    return reduce(add, token_gen(string), [])
