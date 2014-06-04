from ..utils import match, consmap
from ..struct.env import Env
from ..struct.pair import Pair, Empty

line = []
called = False
val = None
add, analysis = match()


def sign(test):
    def inner(handler):
        add(test, handler)
        return handler
    return inner


def normal(handler):
    def wrap(env, pc):
        global val
        val = handler(env)
        pc += 1
        return env, pc
    return wrap


def bind(env, formal, actual):
    while True:
        if isinstance(formal, Pair):
            env[formal.car] = actual.car
            formal = formal.cdr
            actual = actual.cdr
        elif isinstance(actual, Empty):
            break
        else:
            env[formal] = actual


@sign(lambda e: isinstance(e, Pair))
def application(expr):
    operator = expr.car
    operand = expr.cdr
    analysis(operand)
    for e in operand:
        analysis(e)

    def analyzed(env, pc):
        function = env.runtime[operator]
        args = consmap(lambda k: env.runtime[k], operand)
        if called is True:
            global called, val
            called = False
            env[expr] = val
            return env, pc+1
        env = Env(env)
        env.rtn = (env.parent, pc)
        bind(env, function.args, args)
        return env, function.pc


class Return:
    def __call__(self, env, pc):
        # env.rtn is tuple : (env, pc)
        global called
        called = True
        return env.rtn


def analyzer(expr):
    analysis(expr)

    def execute(env, cont):
        line.clear()
        env.rtn = (None, None)  # top
        pc = 0  # program counter
        while env is not None:
            env, pc = line[pc](env, pc)
        return cont(env.val)
    return execute


def eval(expr, env, cont=print):
    analyzer(expr)(env, cont)
