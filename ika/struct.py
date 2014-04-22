class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance


class Flag():
    pass


pyapply_flag = Flag()


class Ptr:
    ptr = None

    def __init__(self, data):
        self.ptr = data


class Tree:
    def __init__(self, data=None, parent=None):
        self.data = data
        self.parent = parent


class Analyzed:

    def __init__(self, raw, analyzed, table=()):
        self.analyzed = analyzed
        self.table = table
        self.raw = raw

    @property
    def name(self):
        return self.analyzed.__module__

    def __call__(self, env):
        now = self
        while isinstance(now, Analyzed):
            now = now.call(env)
        return now

    def call(self, env):
        return self.analyzed(env)


class ReprMixin:
    def __str__(self):
        return repr(self)


class Symbol:
    def __init__(self, string):
        self._string = string

    def __str__(self):
        return self._string

    def __repr__(self):
        return "`" + str(self)


class Boolean:
    pass


class T(ReprMixin, Singleton, Boolean):
    def __repr__(self):
        return "#t"

    def __bool__(self):
        return True


class F(ReprMixin, Singleton, Boolean):
    def __repr__(self):
        return "#f"

    def __bool__(self):
        return False


class List:
    pass


class EmptyList(ReprMixin, Singleton, List):
    def __repr__(self):
        return "()"

    def __bool__(self):
        return False

    def __iter__(self):
        return self

    def __next__(self):
        raise StopIteration

t = T()
f = F()
empty = EmptyList()


class Pair(ReprMixin, List):
    def __init__(self, car, cdr=empty):
        self.car = car
        self.cdr = cdr

    def append(self, obj):
        self.cdr = Pair(obj)

    @property
    def cdar(self):
        return self.cdr.car

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

    def __iter__(self):
        self.it = self
        return self

    def __next__(self):
        if self.it is empty:
            del self.it
            raise StopIteration
        result = self.it.car
        self.it = self.it.cdr
        return result


class Procedure(ReprMixin):
    formal_args = None
    body = None
    _closure = {}

    def __init__(self, closure, formal_args, body):
        self.formal_args = formal_args
        self.body = body
        self._closure = closure

    def __call__(self, env):
        self.body(env)

    def __repr__(self):
        return "#<procedure>"

    def closure(self, env):
        env.data.update(self._closure)
        return env


from .utils import dict_map


class Env(Tree):
    def __init__(self, parent=None, dict_=None):
        if dict_ is None:
            dict_ = dict()
        super(Env, self).__init__(dict_map(Ptr, dict_), parent)

    def get(self, key):
        now = self
        while now:
            if key in now.data:
                return now.data[key]
            now = now.parent
        return None

    def __getitem__(self, key):
        r = self.get(key)
        if r is None:
            raise NameError("name %s not found." % key)
        else:
            return r.ptr

    def __setitem__(self, k, v):
        self.data[k] = Ptr(v)

    def __contains__(self, k):
        now = self
        while now:
            if k in now.data:
                return True
        return False

    def extend(self):
        env = Env(self)
        return env

    def update(self, dict_=None):
        self.data.update(dict_map(Ptr, dict_))

    def clear(self):
        self.data.clear()
