from . import self_evaluating, application


def condition(expr):
    return type(expr) is str and not self_evaluating.condition(expr)\
        and not application.condition(expr)


def analyze(analyzer, expr):
    def analyzed(env):
        return env[expr]
    return analyzed
