from ..utils import tagged, get_operand
from ..struct import f, empty, Analyzed


def analyze(analyzer, expr):
    if not tagged(expr, "if"):
        return None

    expr = get_operand(expr)
    test = analyzer(expr.car)
    consequent = analyzer(expr.cdar)
    alternate = expr.cdr.cdr
    if alternate is not empty:
        alternate = analyzer(alternate.car)

    def analyzed(env):
        if test(env) is not f:
            return consequent
        elif alternate is not empty:
            return alternate
        else:
            return empty
    return Analyzed(__name__, analyzed, (test, consequent, alernate))
