from ..utils import tagged, get_operand, cons_map


def condition(expr):
    return tagged(expr, "begin")


def analyze(analyzer, expr):
    seq = cons_map(analyzer, get_operand(expr))

    def analyzed(env):
        for i in seq:
            r = i(env)
        return r
    return analyzed
