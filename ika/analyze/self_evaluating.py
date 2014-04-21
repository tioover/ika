from ..struct import List, t, f, Analyzed
from ..const import float_pattern

type_dict = {
    lambda e: e[0] == e[-1] == '"': eval,
    lambda e: e.isdigit(): int,
    lambda e: float_pattern.match(e): float,
    lambda e: e == "#t": lambda e: t,
    lambda e: e == "#f": lambda e: f,
}


def condition(expr):
    if isinstance(expr, List):
        return False
    for f in type_dict:
        if f(expr):
            return type_dict[f]
    return False


def analyze(analyzer, expr):
    convert = condition(expr)
    if convert is False:
        return None

    def analyzed(env):
        return convert(expr)
    return Analyzed(__name__, analyzed)
