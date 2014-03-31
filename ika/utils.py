def dict_map(func, dict_):
    for k in dict_:
        dict_[k] = func(dict_[k])
    return dict_


from .struct import Pair, empty


def tagged(expr, name):
    return isinstance(expr, Pair) and get_operator(expr) == name


def get_operator(expr):
    return expr.car


def get_operand(expr):
    return expr.cdr


def cons_map(f, p):
    if p is empty:
        return p
    return Pair(f(p.car), cons_map(f, p.cdr))
