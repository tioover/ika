from .analyze import application, assignment, begin, cond, definition,\
    if_, lambda_, quoted, self_evaluating, variable, pyapply


def judgement(expr):
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
            return handler
    raise ValueError("expr can't inpterpretation.")


def analyzer(expr):
    return judgement(expr).analyze(analyzer, expr)


def eval_(s_exp, env, end=None):
    rtn = analyzer(s_exp)(env)
    if end:
        end(rtn)
