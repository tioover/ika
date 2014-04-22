from ..utils import tagged, analysis
from ..struct import Pair, Symbol, empty
from . import self_evaluating, analyzer

def analyze(expr):
    if not tagged(expr, "quote"):
        return None

    return quote(analyzer, expr.cdar)

@analysis
def quote(expr):
    def analyzed(env):
        if isinstance(expr, Pair):
            return Pair(
                        quote(expr.car)(env),
                        quote(expr.cdr)(env))
        elif self_evaluating.condition(expr):
            return self_evaluating.analyze(expr)(env)
        elif expr is empty:
            return expr
        else:
            return Symbol(expr)
    return analyzed
