from ..struct import empty, f, pyapply_flag
from ..utils import tagged, get_operand, get_operator, cons_map, analysis
from ..procs import base


@analysis
def variable(analyzer, expr):
    if not isinstance(expr, str):
        return None

    def analyzed(env):
        return env[expr]
    return analyzed


@analysis
def begin(analyzer, expr):
    if not tagged(expr, "begin"):
        return None

    seq = cons_map(analyzer, get_operand(expr))

    def analyzed(env):
        while seq.cdr is not empty:
            seq(env)
        return seq.car
    return analyzed


@analysis
def definition(analyzer, expr):
    if not tagged(expr, "define"):
        return None

    def analyzed(env):
        args = get_operand(expr)
        env[args.car] = analyzer(args.cdar)(env)
        return empty
    return analyzed


@analysis
def if_(analyzer, expr):
    if not tagged(expr, "if"):
        return None

    expr = get_operand(expr)
    test = analyzer(expr.car)
    consequent = analyzer(expr.cdar)
    alternate = expr.cdr.cdr
    if alternate is not empty:
        alternate = analyzer(alternate.car)

    def analyzed(env):
        if test(env) is not f:
            return consequent
        elif alternate is not empty:
            return alternate
        else:
            return empty
    return analyzed


@analysis
def pyapply(analyzer, expr):
    if not tagged(expr, pyapply_flag):
        return None

    expr = get_operand(expr)
    func = base[get_operator(expr)]
    args = cons_map(analyzer, get_operand(expr))

    def analyzed(env):
        return func(*list(cons_map(lambda a: a(env), args)))

    return analyzed

from .application import analyze as application
from .lambda_ import analyze as lambda_
from .quoted import analyze as quoted
from .self_evaluating import analyze as self_evaluating

pipeline = [
    self_evaluating,
    variable,
    definition,
    quoted,
    lambda_,
    if_,
    begin,
    pyapply,
    application,
]