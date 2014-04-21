from ..utils import tagged
from ..struct import Pair, Symbol, empty, Analyzed
from . import self_evaluating

def analyze(analyzer, expr):
    if not tagged(expr, "quote"):
        return None

    return quote(analyzer, expr.cdar)


def quote(analyzer, expr):
    def analyzed(env):
        if isinstance(expr, Pair):
            return Pair(quote(analyzer, expr.car)(env),
                        quote(analyzer, expr.cdr)(env))
        elif self_evaluating.condition(expr):
            return self_evaluating.analyze(analyzer, expr)(env)
        elif expr is empty:
            return expr
        else:
            return Symbol(expr)
    return Analyzed(__name__, analyzed)
