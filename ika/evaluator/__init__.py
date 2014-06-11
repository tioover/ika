from ika.struct.types import Cont
from ..struct import Pair, Identifier, Function, empty
from .backend import Env, sign, register, car_is, compile, rtn
from . import instruction


@sign(lambda e: isinstance(e, Identifier))
@register
def name(expr, ir):
    return instruction.name, (expr,)


@sign(lambda e: not isinstance(e, Pair))
@register
def self_evaluator(expr, ir):
    return instruction.self_evaluator, (expr,)


@sign(car_is('define'))
@register
def definition(expr, ir):
    key = expr.cdr.car
    ir.append((instruction.define_empty, (key,)))
    value = expr.cdr.cdr.car
    compile(value, ir)
    return instruction.set_value, (key,)


@sign(car_is('set!'))
@register
def assign(expr, ir):
    key = expr.cdr.car
    value = expr.cdr.cdr.car
    compile(value, ir)
    return instruction.set_value, (key,)


@sign(car_is('begin'))
@register
def begin(expr, ir):
    expr = expr.cdr
    n = 0
    for e in expr:
        compile(e, ir)
        n += 1
    return instruction.begin, (n,)


@sign(car_is('call/cc'))
def callcc(expr, ir):
    ir.append((instruction.callcc, ()))
    compile(expr.cdr.car, ir)
    ir.append((instruction.apply, (ir, 1, True)))


@sign(car_is('lambda'))
def lambda_(expr, ir):
    pc = len(ir)
    ir.append(None)  # Placeholder

    args = expr.cdr.car
    body = expr.cdr.cdr
    func = Function(args, pc+1)

    compile(Pair('begin', body), ir)
    ir.append((rtn, ()))
    i = len(ir)  # skip function body.

    ir[pc] = (instruction.lambda_, (i, body, func))


@sign(lambda e: True)
@register
def application(expr, ir):
    operator = expr.car
    operand = expr.cdr

    unbound = 0
    for e in operand:
        compile(e, ir)
        unbound += 1
    compile(operator, ir)
    return instruction.apply, (ir, unbound)


def output(expr):
    if expr is not empty:
        print(expr)


def evaluator(cont=output):
    ir = []
    env_ = Env()

    def eval_(expr):
        pc = len(ir)
        env = env_
        values = ()

        if expr is not None:
            compile(expr, ir)
        ir.append((rtn, ()))
        while True:
            function, arguments = ir[pc]
            print(pc, values, function)
            if function is rtn and env.parent is None:
                break
            elif function is instruction.self_evaluator:
                pc += 1
                values = (arguments[0], values)
            else:
                env, pc, values = function(env, pc, values, *arguments)
            print(values)
        return cont(values[0])
    return eval_
