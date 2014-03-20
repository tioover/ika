import types
import analyze


def analyzer(expr):
    pipeline = filter(
        lambda x: isinstance(x, types.ModuleType),
        map(lambda x: getattr(analyze, x),
            dir(analyze)))

    for handler in pipeline:
        if handler.condition(expr):
            return handler.analyze(analyzer, expr)


def eval(eval_func, env):
    return analyze(env)


def apply(proc, args):
    pass
