import re
from functools import reduce

token_patterns = [  # TODO: ,() '() #() ,@()
    r"\(",
    r"\)",

    r"'\(",  # quote
    r"`\(",
    r",\(",
    r",@\(",

    r"#\(",  # vector
    "\"(\\\\\"|[^\"])*\"",  # string
    "[^(\\\)|\"|\s)]+",  # name
]

token_re = list(map(re.compile, token_patterns))  # compile patterns.
space_re = re.compile(r"^\s+")


def token_gen(string):
    while string:
        string = space_re.sub("", string)  # remove space.
        match = None
        for re_obj in token_re:
            match = re_obj.match(string)
            if match is not None:
                yield string[:match.end()]
                string = string[match.end():]
                break
        if match is None:
            raise SyntaxError("Can't recognize token: %s" % string)


def lexer(string):
    def add(li, token):
        li.append(token)
        return li
    return reduce(add, token_gen(string), [])
