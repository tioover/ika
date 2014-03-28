from ..utils import tagged
from ..struct import Procedure, Pair, Analyzed
from . import begin


def condition(expr):
    return tagged(expr, "lambda")


def analyze(analyzer, expr):
    args = expr.cdar
    body = begin.analyze(analyzer, Pair("begin", expr.cdr.cdr))

    def analyzed(env):
        # TODO improve lexical closure.
        return Procedure(env, args, body)
    return Analyzed(__name__, analyzed)
