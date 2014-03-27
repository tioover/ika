import re
from ..struct import empty, t, f

number_pattern = re.compile('\d+(\.\d+)?$')


def convert_number(expr):
    if expr.isdigit():
        return int(expr)
    else:
        return float(expr)

type_table = [
    # (judgement, convert),
    # string
    (lambda e: e[0] == e[-1] == '"', eval),
    # number
    (lambda e: number_pattern.match(e), convert_number),
    # ()
    # (lambda e: e == "()", lambda e: empty),
    # true
    (lambda e: e == "#t", lambda e: t),
    # false
    (lambda e: e == "#f", lambda e: f),
]


def condition(expr):
    if type(expr) is not str:
        return False
    else:
        return list(filter(lambda i: i[0](expr), type_table))


def analyze(analyzer, expr):
    for i in type_table:
        if i[0](expr):
            break

    def analyzed(env):
        return i[1](expr)
    return analyzed
