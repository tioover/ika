from ..utils import tagged
from ..struct import empty


def condition(expr):
    return tagged(expr, "define")


def analyze(analyzer, expr):
    def analyed(env):
        env[expr.cdr.car] = analyzer(expr.cdr.cdr.car)(env)
        return empty
    return analyed
