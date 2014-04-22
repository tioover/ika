from ..utils import tagged, analysis
from ..struct import Procedure, Pair
from . import begin


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


@analysis
def analyze(analyzer, expr):
    if not tagged(expr, "lambda"):
        return None

    args = expr.cdar
    body = begin(analyzer, Pair("begin", expr.cdr.cdr))

    def analyzed(env):
        return Procedure(closure(env, expr), args, body)
    return analyzed
