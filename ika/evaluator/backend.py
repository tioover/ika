line = []

add = lambda *x: line.append(x)


def compile(expr, ir):
    for cond, handler in line:
        if cond(expr):
            return handler(expr, ir)


def car_is(*name):
    def wrap(expr):
        for i in name:
            if expr[0] == i:
                return True
        return False
    return wrap


def rtn(env, pc, values):
    assert values[1] == ()
    pc, rtn_values = env.rtn
    return env.parent, pc, (values[0], rtn_values)


class Ref:
    def __init__(self, value):
        self.value = value


class Env:
    def __init__(self, parent=None):
        self.parent = parent
        self.data = {}
        self.rtn = (None, None)

    def __getitem__(self, k):
        return self.data[k].value

    def __setitem__(self, k, v):
        self.data[k] = Ref(v)

    def set_ref(self, k, v):
        ref = self.get_ref(k)
        if ref is not None:
            ref.value = v
        else:
            raise NameError('%s is not defined.' % k)

    def get_ref(self, k, default=None):
        st = self
        while st:
            if k in st.data:
                return st.data[k]
            st = st.parent
        return None


def sign(test):
    def middle(handler):
        add(test, handler)
        return handler
    return middle


def register(handler):
    def wrap(expr, ir):
        command = handler(expr, ir)
        ir.append(command)
        return command
    return wrap
