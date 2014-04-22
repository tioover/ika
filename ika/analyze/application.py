from ..struct import List, empty, Procedure, Analyzed
from ..utils import get_operand, get_operator, cons_map, analysis


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


@analysis
def analyze(analyzer, expr):
    if not condition(expr):
        return None

    operator = analyzer(get_operator(expr))
    operand = cons_map(analyzer, get_operand(expr))

    return (
        lambda env: tail_call_loop(env, operator, operand),
        (operator, operand),
    )


def tail_call_loop(env, operator, operand):
    now = None
    while True:
        func = operator(env)
        if not isinstance(func, Procedure):
            raise TypeError("%s is not procedure." % str(operator))
        args = cons_map(lambda a: a(env), operand)

        if now is None:  # first loop.
            now_env = env.extend()
            now = func.body

        now_env.clear()
        now_env = func.closure(now_env)
        now_env.update(arg_zip(func.formal_args, args))

        while isinstance(now, Analyzed):
            if now.name != __name__:
                now = now.analyzed(now_env)
            else:
                operator, operand = now.table
                break  # skip else.
        else:  # type(now) is not Analyzed.
            break

    return now
