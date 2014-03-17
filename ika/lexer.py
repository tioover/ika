import re
token_patterns = [
    r"\(",
    r"\)",
    r"`\(",  # quote
    r"#\(",  # vector
    "\"[^\"]\"",  # string
    "\'[^\']\'",  # string TODO: \"
    r"\w+",  # name
]

token_re = list(map(re.compile, token_patterns))  # compile patterns.
space_re = re.compile(r"^\s+")


def lexer(string):
    lexed = []  # result
    while string:
        string = space_re.sub("", string)  # remove space.
        for re_obj in token_re:
            match = re_obj.match(string)
            if match:
                lexed.append(string[:match.end()])
                string = string[match.end():]
                break
    return lexed
