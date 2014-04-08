import re
from functools import reduce
from .const import token_patterns, remove_pattern

# compile patterns.
compile = lambda patterns: list(map(re.compile, patterns))
token_res = compile(token_patterns)
remove_re = re.compile(remove_pattern)


def token_gen(raw):
    while raw:
        # remove space and comment.
        remove_match = remove_re.match(raw)
        if remove_match:
            raw = raw[remove_match.end():]
            continue

        for sre in token_res:
            match = sre.match(raw)
            if match is not None:
                yield raw[:match.end()]  # return matched token.
                raw = raw[match.end():]  # split raw.
                break  # stop!

        if match is None:  # raw is not "", and nothing matched.
            raise SyntaxError("Can't recognize token: %s" % raw)


def lexer(string):
    def add(li, token):
        li.append(token)
        return li
    return reduce(add, token_gen(string), [])
