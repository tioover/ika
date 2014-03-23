import types
from . import analyze


def analyzer(expr):
    pipeline = filter(
        lambda x: isinstance(x, types.ModuleType),
        map(lambda x: getattr(analyze, x),
            dir(analyze)))

    for handler in pipeline:
        if handler.condition(expr):
            return handler.analyze(analyzer, expr)


def eval(s_exp, env, end):
    end(analyzer(s_exp)(env))


def apply(proc, args):
    pass
