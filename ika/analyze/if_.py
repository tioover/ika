from ..utils import tagged, get_operand
from ..struct import f, empty


def condition(expr):
    return tagged(expr, "if")


def analyze(analyzer, expr):
    expr = get_operand(expr)
    test = analyzer(expr.car)
    consequent = analyzer(expr.cdar)
    alternate = expr.cdr.cdr
    if alternate is not empty:
        alternate = analyzer(alternate.car)

    def analyzed(env):
        if test(env) is not f:
            return consequent(env)
        elif alternate is not empty:
            return alternate(env)
        else:
            return empty
    return analyzed
