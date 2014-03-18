import re
from functools import reduce
from .const import transfrom

token_patterns = [
    "(",
    ")",
]
token_patterns.extend(transfrom.keys())
token_patterns = list(map(re.escape, token_patterns))  # escape for re.
token_patterns.extend(  # complex re expr, can't escape.
    [
        r'"(\\"|[^"])*"',  # string
        r'[^(\)|"|\s)]+',  # name
    ]
)

# compile patterns.
token_re = list(map(re.compile, token_patterns))
space_re = re.compile(r"^\s+")


def token_gen(string):
    while string:
        string = space_re.sub("", string)  # remove space in string start.
        match = None  # re.match result.
        for re_obj in token_re:
            match = re_obj.match(string)
            if match is not None:
                yield string[:match.end()]  # return matched token.
                string = string[match.end():]  # split string.
                break  # stop!
        if match is None:  # nothing matched.
            raise SyntaxError("Can't recognize token: %s" % string)


def lexer(string):
    def add(li, token):
        li.append(token)
        return li
    return reduce(add, token_gen(string), [])
