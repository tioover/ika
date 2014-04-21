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
        analyzed = handler.analyze(analyzer, expr)
        if analyzed:
            return analyzed
    else:
        raise ValueError("expr can't inpterpretation.")


def eval_(s_exp, env, end=None):
    result_value = analyzer(s_exp)(env)
    if end is not None:
        print(result_value)
