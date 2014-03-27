import re
from ..struct import Pair, empty, t, f

number_pattern = re.compile('\d+(\.\d+)?$')


def convert_number(expr):
    if expr.isdigit():
        return int(expr)
    else:
        return float(expr)

type_table = [
    # (judgement, convert),
    # empty
    (lambda e: e is empty, lambda x: x),
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
    if isinstance(expr, Pair):
        return False
    for i in type_table:
        if i[0](expr):
            return True
    return False


def analyze(analyzer, expr):
    for i in type_table:
        if i[0](expr):
            break

    def analyzed(env):
        return i[1](expr)
    return analyzed
