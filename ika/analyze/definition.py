from ..utils import tagged, get_operand
from ..struct import empty


def condition(expr):
    return tagged(expr, "define")


def analyze(analyzer, expr):
    def analyed(env):
        args = get_operand(expr)
        env[args.car] = analyzer(args.cdar)(env)
        return empty
    return analyed
