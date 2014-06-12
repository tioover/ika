class Pair(tuple):
    def __repr__(self):
        car, cdr = self
        expr = '(%s' % repr(car)
        while isinstance(cdr, Pair):
            car, cdr = cdr
            expr += ' ' + repr(car)
        if cdr is ():
            expr += ')'
        else:
            expr += ' . %s)' % repr(cdr)
        return expr


def pair_iter(pair):
    cdr = pair
    while isinstance(cdr, Pair):
        car, cdr = cdr
        yield car


def lst(*items, tail=()):
    items = tuple(items)
    tail = Pair(items[-1], tail)
    now = tail
    i = len(items) - 2
    while i >= 0:
        now = Pair(items[i], now)
        i -= 1
    return now
