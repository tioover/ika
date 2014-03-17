from numpy import array
from .struct import t, f


def is_true(atom):
    if atom is f:
        return f
    else:
        return t


def is_false(atom):
    if atom is f:
        return t
    else:
        return f


def cons(x, y):
    return array([x, y])


def car(x):
    return array[0]


def cdr(x):
    return array[1]
