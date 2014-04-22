def analyzer(expr):
    from .analyze import pipeline
    for handler in pipeline:
        analyzed = handler(expr)
        if analyzed:
            return analyzed
    else:
        raise ValueError("expr can't inpterpretation.")


def eval_(s_exp, env, end=None):

    result_value = analyzer(s_exp)(env)
    if end is not None:
        print(result_value)
