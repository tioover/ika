from ..struct import List, t, f
from ..const import float_pattern
from ..utils import analysis

type_tuple = (
    (lambda e: e[0] == e[-1] == '"', eval),
    (lambda e: e.isdigit(), int),
    (lambda e: float_pattern.match(e), float),
    (lambda e: e == "#t", lambda e: t),
    (lambda e: e == "#f", lambda e: f),
)


def condition(expr):
    if isinstance(expr, List):
        return False
    for f, g in type_tuple:
        if f(expr):
            return g
    return False


@analysis
def analyze(expr):
    convert = condition(expr)
    if convert is False:
        return None

    def analyzed(env):
        return convert(expr)
    return analyzed
