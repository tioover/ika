from ..utils import tagged, get_operand
from ..struct import Pair, empty


def condition(expr):
    return tagged(expr, "begin")


def analyze(analyzer, expr):
    seq = get_operand(expr)

    def analyzed(env):
        if not isinstance(seq, Pair):
            return analyzer(seq)(env)
        r = analyzer(seq.car)(env)
        if seq.cdr is empty:
            return r
        else:
            return analyze(analyzer, seq.cdr)(env)
    return analyzed
