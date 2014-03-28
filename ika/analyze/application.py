from ..struct import List, empty, Procedure, Analyzed
from ..utils import get_operand, get_operator, cons_map


def condition(expr):
    return isinstance(expr, List)


def arg_zip(formal, actul, dct=None):
    if dct is None:
        dct = {}

    if not isinstance(formal, List):  # a
        dct[formal] = actul
        return dct
    elif formal is empty:
        if actul is empty:
            return dct
        else:
            raise TypeError("Too more actul arguments.")
    elif not isinstance(formal.cdr, List):  # (a . b)
        dct[formal.cdr] = actul
    elif actul is empty:
        raise TypeError("Too less actul arguments.")
    else:  # normal
        dct[formal.car] = actul.car
    return arg_zip(formal.cdr, actul.cdr, dct)


def analyze(analyzer, expr):
    if expr is empty:
        raise SyntaxError("illegal empty application.")

    operator = analyzer(get_operator(expr))
    operand = cons_map(analyzer, get_operand(expr))

    def analyzed(env):
        func = operator
        args = operand
        body = True  # loop once flag

        while body or isinstance(body, Analyzed):
            body = False
            operator_ = func(env)
            operand_ = cons_map(lambda a: a(env), args)
            body = operator_.body
            if not isinstance(operator_, Procedure):
                raise TypeError("%s is not procedure." % str(operator_))
            env = operator_.env.extend(
                arg_zip(operator_.formal_args, operand_))
            if body.name == __name__:
                func, args = body.raw
            else:
                body = body.func(env)

        return body

    return Analyzed(__name__, analyzed, (operator, operand))
