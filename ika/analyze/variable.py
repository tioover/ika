from . import self_evaluating, application
from ..struct import Analyzed


def condition(expr):
    return type(expr) is str and not self_evaluating.condition(expr)\
        and not application.condition(expr)


def analyze(analyzer, expr):
    if not condition(expr):
        return None

    def analyzed(env):
        return env[expr]
    return Analyzed(__name__, analyzed)
