from ..utils import tagged, get_operand
from ..struct import empty, Analyzed


def condition(expr):
    return tagged(expr, "define")


def analyze(analyzer, expr):
    def analyzed(env):
        args = get_operand(expr)
        env[args.car] = analyzer(args.cdar)(env)
        return empty
    return Analyzed(__name__, analyzed)
