class Empty(tuple):
    def __repr__(self):
        return '()'
empty = Empty()


class Pair(tuple):
    def __new__(cls, pair=empty):
        if pair is empty:
            return pair
        assert len(pair) == 2
        return super(Pair, cls).__new__(cls, pair)

    @property
    def car(self):
        return self[0]

    @property
    def cdr(self):
        return self[1]

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


def cons(car, cdr):
    return Pair((car, cdr))


def lst(items):
    items = list(items)
    tail = cons(items[-1], empty)
    now = tail
    i = len(items) - 2
    while i >= 0:
        now = cons(items[i], now)
    return now
