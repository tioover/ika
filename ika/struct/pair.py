class Empty(tuple):
    def __repr__(self):
        return '()'
empty = Empty()


class Pair(tuple):
    def __new__(cls, *args, **kwargs):
        if not args or args[0] is empty:
            return empty
        return super(Pair, cls).__new__(cls, *args, **kwargs)

    @property
    def car(self):
        return self[0]

    @property
    def cdr(self):
        return self[1]

    def __repr__(self, start=True):
        car = self.car
        cdr = self.cdr
        if isinstance(cdr, Pair):
            expr = '%s %s' % (repr(car), cdr.__repr__(start=False))
        elif cdr is empty:
            expr = '%s)' % repr(car)
        else:
            expr = '%s . %s)' % (repr(car), repr(cdr))
        if start:
            expr = '(' + expr
        return expr
