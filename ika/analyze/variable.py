from . import self_evaluating


def condition(expr):
    return type(expr) is str and not self_evaluating.condition(expr)


def analyze(analyzer, expr):
    def analyzed(env):
        return env[expr]
    return analyzed
