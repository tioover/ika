from .struct import empty


def cons_iter(x):
    while x is not empty:
        yield x.car
        x = x.cdr
