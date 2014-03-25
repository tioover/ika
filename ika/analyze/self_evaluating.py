import re
from ..struct import empty, t, f

number_pattern = re.compile('\d+(\.\d+)?$')


def convert_number(expr):
    if expr.isdigit():
        return int(expr)
    else:
        return float(expr)

type_table = [
    # (judgment, convert),
    (lambda e: e[0] == e[-1] == '"', str),  # string
    (lambda e: number_pattern.match(e), convert_number),  # number
    (lambda e: e == "()", lambda e: empty),  # ()
    (lambda e: e == "#t", lambda e: t),  # true
    (lambda e: e == "#f", lambda e: f),  # false
]


def condition(expr):
    return list(filter(lambda i: i[0](expr), type_table))


def analyze(analyzer, expr):
    for i in type_table:
        if i[0](expr):
            break
    return i[1](expr)
