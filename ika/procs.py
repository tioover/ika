from .struct import t, f, empty


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


def is_null(atom):
    if atom is empty:
        return t
    else:
        return f
