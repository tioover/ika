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


class Status:
    ''' Status tree. '''
    def __init__(self, parent=None):
        self.parent = parent
        self.env = {}
        self.values = []
        self.rtn = None


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
        # for i, item in enumerate(ir):
        #     print(i, item)
        pc = i  # program counter
        while pc < len(ir):
            # print('DEBUG: PC', pc, st.values, ir[pc])
            st, pc = ir[pc](st, pc)
        value = st.values.pop()
        return cont(value)
    return execute
