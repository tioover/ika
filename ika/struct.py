class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance


class Tree:
    def __init__(self, data=None, parent=None):
        self.data = data
        if parent:
            parent.children.append(self)
        self.parent = parent


class Env(Tree):
    def __init__(self, dict_={}, parent=None):
        super(Env, self).__init__(dict_, parent)

    def __getitem__(self, key):
        now = self
        while now:
            if key in now.data:
                return now.data[key]
            now = now.parent
        raise NameError("name %s not found." % key)

    def __setitem__(self, k, v):
        self.data[k] = v


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
        return "#t"

    def __bool__(self):
        return True


class F(ReprMixin, Singleton):
    def __repr__(self):
        return "#f"

    def __bool__(self):
        return False


class EmptyList(ReprMixin, Singleton):
    def __repr__(self):
        return "()"

t = T()
f = F()
empty = EmptyList()


class Pair(ReprMixin):
    def __init__(self, car, cdr=empty):
        self.car = car
        self.cdr = cdr

    def append(self, obj):
        self.cdr = Pair(obj)

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
            string = "(%s . %s)" % (car_str, repr(self.cdr))  # little bug.
        return string
