from ..utils import tagged
from ..struct import Procedure, Pair, Analyzed
from . import begin


def condition(expr):
    return tagged(expr, "lambda")


def closure(env, expr, var=None):
    if not var:
        var = {}
    for now in expr:
        if isinstance(now, Pair):
            closure(env, now, var)
        else:
            name = now
            val = env.get(name)
            if val is not None:
                var[name] = val
    return var


def analyze(analyzer, expr):
    args = expr.cdar
    body = begin.analyze(analyzer, Pair("begin", expr.cdr.cdr))

    def analyzed(env):
        return Procedure(closure(env, expr), args, body)
    return Analyzed(__name__, analyzed, (args, body))
