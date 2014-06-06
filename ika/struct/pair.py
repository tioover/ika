from .base import Singleton


class Empty(Singleton):
    def __repr__(self):
        return '()'

    def __iter__(self):
        return self

    def __next__(self):
        raise StopIteration

empty = Empty()


class Pair:
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr

    def __repr__(self):
        car, cdr = self.car, self.cdr
        expr = '(%s' % repr(car)
        while isinstance(cdr, Pair):
            expr += ' ' + repr(cdr.car)
            cdr = cdr.cdr
        if cdr is empty:
            expr += ')'
        else:
            expr += ' . %s)' % repr(cdr)
        return expr

    def __iter__(self):
        while isinstance(self, Pair):
            yield self.car
            self = self.cdr


def lst(*items, tail=empty):
    items = tuple(items)
    tail = Pair(items[-1], tail)
    now = tail
    i = len(items) - 2
    while i >= 0:
        now = Pair(items[i], now)
        i -= 1
    return now
