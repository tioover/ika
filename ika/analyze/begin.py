from ..struct import Analyzed, empty
from ..utils import tagged, get_operand, cons_map


def condition(expr):
    return tagged(expr, "begin")


def analyze(analyzer, expr):
    seq = cons_map(analyzer, get_operand(expr))

    def analyzed(env):
        while seq.cdr is not empty:
            seq(env)
        return seq.car
    return Analyzed(__name__, analyzed)
