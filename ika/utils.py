from procs import car, cdr
from struct import nil


def cons_iter(x):
    while x is not nil:
        yield car(x)
        cdr(x)
