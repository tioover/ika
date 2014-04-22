from ..struct import empty
from ..utils import tagged, get_operand, cons_map, analysis


@analysis
def analyze(analyzer, expr):
    if not tagged(expr, "begin"):
        return None

    seq = cons_map(analyzer, get_operand(expr))

    def analyzed(env):
        while seq.cdr is not empty:
            seq(env)
        return seq.car
    return analyzed
