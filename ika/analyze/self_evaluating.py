from ..struct import List, t, f, Analyzed
from ..const import float_pattern


type_table = [
    # (judgement, convert),
    # string
    (lambda e: e[0] == e[-1] == '"', eval),
    # int
    (lambda e: e.isdigit(), int),
    # float
    (lambda e: float_pattern.match(e), float),
    # true
    (lambda e: e == "#t", lambda e: t),
    # false
    (lambda e: e == "#f", lambda e: f),
]


def condition(expr):
    if isinstance(expr, List):
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
    return Analyzed(__name__, analyzed)
