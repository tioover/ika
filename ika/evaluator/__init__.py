from ..utils import match
from ..struct.env import Env
from ..struct.pair import Pair, Empty, lst
from ..struct.function import Function
from ..struct.types import Identifier

add, analysis = match()
car_is = lambda x: lambda y, _: y.car == x


class Runtime(dict):
    least = None


def sign(test):
    def inner(handler):
        add(test, handler)
        return handler
    return inner


def register(handler):
    def wrap(expr, line):
        analyzed = handler(expr)
        analyzed.raw = expr
        line.append(analyzed)
        return analyzed
    return wrap


def normal(analyzed):
    def wrap(env, pc, runtime):
        runtime[wrap.raw] = runtime.least = analyzed(env)
        return env, pc+1
    return wrap


def rtn(env, *args):
    return env.parent, env.rtn


@sign(lambda e, _: isinstance(e, Identifier))
@register
def name(expr):
    @normal
    def analyzed(env):
        while env is not None:
            if expr in env:
                return env[expr]
            env = env.parent
    return analyzed


@sign(lambda e, _: not isinstance(e, Pair))
@register
def self_evaluator(expr):
    @normal
    def analyzed(env):
        return expr
    return analyzed


@sign(car_is('lambda'))
def _lambda(expr, line):
    i = len(line)
    line.append(None)

    args = expr.cdr.car
    body = expr.cdr.cdr
    f = Function(args, i+1)
    analysis(body, line)
    line.append(rtn)
    next = len(line)

    def analyzed(env, pc, runtime):
        runtime[expr] = runtime.least = f
        return env, next

    line[i] = analyzed


def argbind(env, runtime, args, operand):
    while True:
        if isinstance(args, Pair):
            env[args.car] = runtime[operand.car]
            args = args.cdr
            operand = operand.cdr
        elif isinstance(args, Empty):
            break
        else:
            env[args] = lst([runtime[k] for k in operand])


@sign(lambda e, _: True)
def application(expr, line):
    operator = expr.car
    operand = expr.cdr
    analysis(operator, line)
    for i in operand:
        analysis(i, line)

    def analyzed(env, pc, runtime):
        function = runtime[operator]
        env = Env(env)
        env.rtn = pc+1
        argbind(env, runtime, function.args, operand)
        return env, function.pc

    def receive(env, pc, runtime):
        env[expr] = runtime.least
        return env, pc+1

    line.append(analyzed)
    line.append(receive)


def analyzer(expr):
    line = []
    analysis(expr, line)
    line.append(rtn)

    def execute(env, cont):
        pc = 0  # program counter
        env.rtn = None  # top
        runtime = Runtime()
        print(line)
        while env is not None:
            print('--')
            print(line[pc], pc)
            if hasattr(line[pc], 'raw'):
                print(line[pc].raw)
            env, pc = line[pc](env, pc, runtime)
            print(pc)
        return cont(runtime.least)
    return execute


def eval(expr, env, cont=print):
    analyzer(expr)(env, cont)
