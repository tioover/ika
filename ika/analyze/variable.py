from . import self_evaluating, application
from ..utils import analysis


def condition(expr):
    return type(expr) is str and not self_evaluating.condition(expr)\
        and not application.condition(expr)


@analysis
def analyze(analyzer, expr):
    if not condition(expr):
        return None

    def analyzed(env):
        return env[expr]
    return analyzed
