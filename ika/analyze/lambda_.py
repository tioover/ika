from ..utils import tagged
from ..struct import Procedure, Pair, Analyzed
from . import begin


def condition(expr):
    return tagged(expr, "lambda")


def analyze(analyzer, expr):
    args = expr.cdar
    body = begin.analyze(analyzer, Pair("begin", expr.cdr.cdr))

    def analyzed(env):
        return Procedure(make_closure(env, expr), args, body)
    return Analyzed(__name__, analyzed, (args, body))


def make_closure(env, expr, var=None):
    if not var:
        var = {}
    for i in expr:
        if isinstance(i, Pair):
            make_closure(env, i, var)
        else:
            r = env.get(i)
            if r is not None:
                var[i] = r
    return var
