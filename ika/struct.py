class Singleton():
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance


class ReprMixin():
    def __str__(self):
        return repr(self)


class Symbol():

    def __init__(self, string):
        self._string = string

    def __str__(self):
        return self._string


class T(ReprMixin, Singleton):
    def __repr__(self):
        "#t"

    def __bool__(self):
        return True


class F(ReprMixin, Singleton):
    def __repr__(self):
        "#f"

    def __bool__(self):
        return False


class EmptyList(ReprMixin, Singleton):
    def __repr__(self):
        return "`()"

t = T()
f = F()
empty = EmptyList()


class Pair(ReprMixin):
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr

    def __repr__(self):
        if type(self.car) is str:
            car_str = "\"%s\"" % repr(self.car)[1:-1]
        else:
            car_str = repr(self.car)

        if type(self.cdr) is Pair:
            string = "(%s %s" % (car_str, repr(self.cdr)[1:])
        elif self.cdr is empty:
            string = "(%s)" % car_str
        else:
            string += "(%s . %s)" % (car_str, repr(self.cdr))
        return string


def cons(x, y):
    return Pair(x, y)


def car(x):
    return x.car


def cdr(x):
    return x.cdr
