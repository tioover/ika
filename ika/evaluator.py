from .analyze import application, assignment, begin, cond, definition,\
    if_, lambda_, quoted, self_evaluating, variable, pyapply


def analyzer(expr):
    pipeline = [
        self_evaluating,
        variable,
        definition,
        quoted,
        lambda_,
        cond,
        if_,
        begin,
        assignment,
        pyapply,
        application,
    ]

    for handler in pipeline:
        if handler.condition(expr):
            return handler.analyze(analyzer, expr)
    raise ValueError("expr can't inpterpretation.")


def eval_(s_exp, env, end=None):
    rtn = analyzer(s_exp)(env)
    if end:
        end(rtn)
