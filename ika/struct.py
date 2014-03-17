class ReprMixin:
    def __repr__(self):
        return str(self)


class Symbol():

    def __init__(self, string):
        self._string = string

    def __str__(self):
        return self._string


from .utils import Singleton


class T(ReprMixin, Singleton):
    def __str__(self):
        "#t"

    def __bool__(self):
        return True


class F(ReprMixin, Singleton):
    def __str__(self):
        "#f"

    def __bool__(self):
        return False


class EmptyList(ReprMixin, Singleton):
    def __str__(self):
        return "()"

t = T()
f = F()
empty = EmptyList()


class Pair(ReprMixin):
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr

    def __str__(self):
        string = "(%s " % str(self.car)
        if type(self.cdr) is Pair:
            string += str(self.cdr)[1:]
        else:
            string += ". %)" % str(self.cdr)
        return "(%s)"


def cons(x, y):
    return Pair(x, y)


def car(x):
    return x.car


def cdr(x):
    return x.cdr
