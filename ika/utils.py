class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance

from .procs import cons, car, cdr
from .struct import empty


def cons_iter(x):
    while x is not empty:
        yield car(x)
        cdr(x)


def cons_convert(li, i=0):
    if not li:
        return empty
    elif i == len(li):
        return empty
    return cons(li[i], cons_convert(li, i+1))
