from ..utils import tagged, get_operand
from ..struct import empty, Analyzed


def analyze(analyzer, expr):
    if not tagged(expr, "define"):
        return None

    def analyzed(env):
        args = get_operand(expr)
        env[args.car] = analyzer(args.cdar)(env)
        return empty
    return Analyzed(__name__, analyzed)
