from ..struct import Pair


def condition(expr):
    return isinstance(expr, Pair) and not isinstance(expr.cdr, Pair)


def analyze(analyzer, expr):
    def analyzed(env):
        return Pair(analyzer(expr.car)(env), analyzer(expr.cdr)(env))
    return analyzed
