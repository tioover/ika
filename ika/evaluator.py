from .analyze import application, assignment, begin, cond, definition,\
    if_, lambda_, quoted, self_evaluating, variable, cons


def pre_interpreter(base_env):
    return base_env


def analyzer(expr):
    pipeline = [
        self_evaluating,
        variable,
        definition,
        begin,
        quoted,
        lambda_,
        cond,
        if_,
        begin,
        assignment,
        cons,
        application,  # must place to end.
    ]

    for handler in pipeline:
        if handler.condition(expr):
            return handler.analyze(analyzer, expr)
    raise ValueError("expr can't inpterpretation.")


def eval(s_exp, env, end):
    end(analyzer(s_exp)(env))
