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
        alternate = alternate.car
    alternate = analyzer(alternate)

    def analyzed(env):
        if test(env) is not f:
            return consequent(env)
        else:
            return alternate(env)
    return analyzed
