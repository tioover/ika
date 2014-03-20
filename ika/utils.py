import os
from .struct import empty


def cons_iter(x):
    while x is not empty:
        yield x.car
        x = x.cdr


def get_module_name(path):
    return map(lambda x: x[0],
               filter(
                   lambda x: x[0] != '__init__' and x[-1] == '.py',
                   map(os.path.splitext,
                       os.listdir(path))))  # This is LISP :)
