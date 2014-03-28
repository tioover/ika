from ..utils import tagged, get_operand, get_operator, cons_map
from ..procs import base
from ..struct import pyapply_flag, Analyzed


def condition(expr):
    return tagged(expr, pyapply_flag)


def analyze(analyzer, expr):
    expr = get_operand(expr)
    func = base[get_operator(expr)]
    args = cons_map(analyzer, get_operand(expr))

    def analyzed(env):
        return func(*list(cons_map(lambda a: a(env), args)))

    return Analyzed(__name__, analyzed)
