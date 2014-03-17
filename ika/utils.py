class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance

from procs import car, cdr
from struct import nil


def cons_iter(x):
    while x is not nil:
        yield car(x)
        cdr(x)
