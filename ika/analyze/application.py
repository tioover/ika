from ..struct import List, empty, Procedure, Analyzed
from ..utils import get_operand, get_operator, cons_map, analysis


def condition(expr):
    if expr is empty:
        raise SyntaxError("illegal empty application.")
    return isinstance(expr, List)


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
    env = env.extend()  # push
    while True:
        func, args = list_eval(env, operator, operand)
        now = func.body
        refresh(env, func, args)

        while isinstance(now, Analyzed):
            if now.name == __name__:
                operator, operand = now.table
                break  # skip else.
            now = now.call(env)
        else:  # type(now) is not Analyzed.
            break

    return now


def list_eval(env, operator, operand):
    func = operator(env)
    if not isinstance(func, Procedure):
        raise TypeError("%s is not procedure." % str(operator))
    args = cons_map(lambda a: a(env), operand)
    return func, args


def refresh(env, func, args):
    env.clear()
    new_value = arg_zip(func.formal_args, args)
    env = func.closure(env)
    env.update(new_value)


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