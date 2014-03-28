from .struct import Pair, Symbol, Boolean, Procedure, f, t, empty


base = {}


def sign(name=None):
    def warp(func):
        k = name
        if k is None:
            k = func.__name__

        def g(*args):
            rtn = func(*args)
            if rtn is True:
                return t
            elif rtn is False:
                return f
            else:
                return rtn

        base[k] = g
        return g
    return warp


@sign()
def add(a, b):
    return a+b


@sign()
def cons(a, b):
    return Pair(a, b)


@sign("eq?")
def eq(a, b):
    return a is b


@sign("boolean?")
def boolean(a):
    return isinstance(a, Boolean)


@sign("pair?")
def pair(a):
    return isinstance(a, Pair)


@sign("symbol?")
def symbol(a):
    return isinstance(a, Symbol)


@sign("char?")
def char(a):
    return isinstance(a, str) and len(a) == 1


@sign("string?")
def string(a):
    return isinstance(a, str) and len(a) > 1


@sign("vector?")
def vector(a):
    return isinstance(a, list)


# TODO port


@sign("procedure?")
def procedure(a):
    return isinstance(a, Procedure)


@sign("null?")
def null(a):
    return a is empty
