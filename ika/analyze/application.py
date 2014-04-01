from ..struct import List, empty, Procedure, Analyzed
from ..utils import get_operand, get_operator, cons_map


def condition(expr):
    return isinstance(expr, List)


def arg_zip(formal, actul, dct=None):
    if dct is None:
        dct = {}

    if actul is not empty:
        if formal is empty:
            raise TypeError("Too more actul arguments.")
        elif not isinstance(formal, List):  # a
            dct[formal] = actul
            return dct
        else:  # normal
            if formal.car in dct:
                raise TypeError("repeat formal argument.")
            dct[formal.car] = actul.car
            return arg_zip(formal.cdr, actul.cdr, dct)
    elif actul is empty:  # else
        if formal is empty:
            return dct
        else:
            raise TypeError("Too less actul arguments.")


def analyze(analyzer, expr):
    if expr is empty:
        raise SyntaxError("illegal empty application.")

    operator = analyzer(get_operator(expr))
    operand = cons_map(analyzer, get_operand(expr))

    return Analyzed(
        __name__,
        lambda env: tail_call_loop(env, operator, operand),
        table=(operator, operand))


def tail_call_loop(env, operator, operand):
    body = None
    while body is None or isinstance(body, Analyzed):
        func = operator(env)
        args = cons_map(lambda a: a(env), operand)
        if not isinstance(func, Procedure):
            raise TypeError("%s is not procedure." % str(operator))
        elif body is None:  # first loop.
            env = env.extend(func.closure)
            body = func.body
        env.update(arg_zip(func.formal_args, args))

        while isinstance(body, Analyzed):
            if body.name == __name__:
                operator, operand = body.table
                break
            else:
                body = body.func(env)
    return body
