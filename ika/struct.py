class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance


class PRE(Singleton):
    '''PRE interpretation flag.'''
    pass


pyapply_flag = PRE()


class Tree:
    children = []

    def __init__(self, data=None, parent=None):
        self.data = data
        if parent:
            parent.children.append(self)
        self.parent = parent


class Analyzed:

    def __init__(self, name, func, table=()):
        self.name = name
        self.func = func
        self.table = table

    def __call__(self, env):
        now = self
        while isinstance(now, Analyzed):
            now = now.func(env)
        return now


class Env(Tree):
    def __init__(self, parent=None, dict_=None):
        if dict_ is None:
            dict_ = dict()
        super(Env, self).__init__(dict_, parent)

    def __getitem__(self, key):
        now = self
        while now:
            print(key)
            if key in now.data:
                return now.data[key]
            now = now.parent
        raise NameError("name %s not found." % key)

    def __setitem__(self, k, v):
        self.data[k] = v

    def extend(self, dict_=None):
        return Env(self, dict_)

    def update(self, dict_=None):
        self.data.update(dict_)


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
    env = None

    def __init__(self, env, formal_args, body):
        self.formal_args = formal_args
        self.body = body
        self.env = env

    def __call__(self, env):
        self.body(env)

    def __repr__(self):
        return "#<procedure>"
