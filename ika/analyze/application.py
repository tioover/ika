from ..struct import List, empty, Procedure, Analyzed
from ..utils import get_operand, get_operator, cons_map


def condition(expr):
    if expr is empty:
        raise SyntaxError("illegal empty application.")
    return isinstance(expr, List)


def arg_zip(formal, actul, dict_=None):
    if dict_ is None:
        dict_ = {}

    if actul is not empty:
        if formal is empty:
            raise TypeError("Too more actul arguments.")
        elif not isinstance(formal, List):  # a
            dict_[formal] = actul
            return dict_
        else:  # normal
            if formal.car in dict_:
                raise TypeError("repeat formal argument.")
            dict_[formal.car] = actul.car
            return arg_zip(formal.cdr, actul.cdr, dict_)
    elif actul is empty:  # else
        if formal is empty:
            return dict_
        else:
            raise TypeError("Too less actul arguments.")


def analyze(analyzer, expr):
    if not condition(expr):
        return None
    operator = analyzer(get_operator(expr))
    operand = cons_map(analyzer, get_operand(expr))

    return Analyzed(
        __name__,
        lambda env: tail_call_loop(env, operator, operand),
        table=(operator, operand))


def tail_call_loop(env, operator, operand):
    now = None
    while True:
        func = operator(env)
        args = cons_map(lambda a: a(env), operand)
        if not isinstance(func, Procedure):
            raise TypeError("%s is not procedure." % str(operator))
        elif now is None:  # first loop.
            env = env.extend(func.closure)
            now = func.body
        env.update(arg_zip(func.formal_args, args))

        while isinstance(now, Analyzed):
            if now.name != __name__:
                now = now.func(env)
            else:
                operator, operand = now.table
                break  # skip else.
        else:  # type(now) is not Analyzed.
            break

    return now
