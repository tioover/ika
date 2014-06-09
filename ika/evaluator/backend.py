line = []

add = lambda *x: line.append(x)


def compile(expr, ir):
    for cond, handler in line:
        if cond(expr):
            return handler(expr, ir)


def car_is(*name):
    def wrap(expr):
        for i in name:
            if expr.car == i:
                return True
        return False
    return wrap


def rtn(st, pc):
    st.parent.values.append(st.values.pop())
    return st.parent, st.rtn

class Ref:
    def __init__(self, value):
        self.value = value


class Status:
    ''' Status tree. '''
    def __init__(self, parent=None):
        self.parent = parent
        self.env = {}
        self.values = []
        self.rtn = None

    def __getitem__(self, k):
        ref = self.getref(k)
        if ref is None:
            raise KeyError('"%d" not in env.' % k)
        return ref.value

    def __setitem__(self, k, v):
        self.env[k] = Ref(v)

    def __call__(self):
        return self.values.pop()

    def setref(self, k, v):
        ref = self.getref(k)
        if ref is not None:
            ref.value = v
        else:
            raise NameError('%s is not defined.' % k)

    def getref(st, k, default=None):
        while st:
            if k in st.env:
                return st.env[k]
            st = st.parent


def sign(test):
    def middle(handler):
        add(test, handler)
        return handler
    return middle


def register(handler):
    def wrap(expr, ir):
        compiled = handler(expr, ir)
        ir.append(compiled)
        return compiled
    return wrap


def normal(f):
    def instruction(st, pc):
        st.values.append(f(st, pc))
        return st, pc+1
    return instruction


def compiler(ir, expr):
    i = len(ir)
    compile(expr, ir)

    def execute(st, cont):
        # print('Expr:')
        # print(expr)
        # print('Instruction:')
        # for n, item in enumerate(ir):
        #     print(n, item)
        pc = i  # program counter
        while pc < len(ir):
            # print('DEBUG: PC', pc, st.values, ir[pc])
            st, pc = ir[pc](st, pc)
        value = st()
        return cont(value)
    return execute
