from ..utils import tagged
from ..struct import Procedure


def condition(expr):
    return tagged(expr, "lambda")


def analyze(analyzer, expr):
    args = expr.cdar
    body = analyzer(expr.cdr.cdr.car)

    def analyzed(env):
        return Procedure(env, args, body)
    return analyzed
