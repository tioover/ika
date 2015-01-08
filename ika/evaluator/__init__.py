from ..struct import Pair, Identifier, Function
from .backend import Env, sign, register, car_is, compiler, rtn
from . import instruction


@sign(lambda e: isinstance(e, Identifier))
@register
def name(expr, _):
    return instruction.name, (expr,)


@sign(lambda e: not isinstance(e, Pair))
@register
def self_evaluator(expr, _):
    return instruction.self_evaluator, (expr,)


@sign(car_is('define'))
@register
def definition(expr, ir):
    key = expr[1][0]  # .cdr.car
    ir.append((instruction.define_empty, (key,)))
    value = expr[1][1][0]  # .cdr.cdr.car
    compiler(value, ir)
    return instruction.set_value, (key,)


@sign(car_is('set!'))
@register
def assign(expr, ir):
    key = expr[1][0]  # .cdr.car
    value = expr[1][1][0]  # .cdr.cdr.car
    compiler(value, ir)
    return instruction.set_value, (key,)


@sign(car_is('begin'))
@register
def begin(expr, ir):
    expr = expr[1]
    n = 0
    while expr:
        e, expr = expr
        compiler(e, ir)
        n += 1
    return instruction.begin, (n,)


@sign(car_is('call/cc'))
def callcc(expr, ir):
    ir.append((instruction.callcc, ()))
    compiler(expr[1][0], ir)
    ir.append((instruction.apply, (ir, 1)))


@sign(car_is('lambda'))
def lambda_(expr, ir):
    pc = len(ir)
    ir.append(None)  # Placeholder

    args, body = expr[1]
    func = Function(args, pc+1)

    compiler(Pair(('begin', body)), ir)
    ir.append((rtn, ()))
    i = len(ir)  # skip function body.

    ir[pc] = (instruction.lambda_, (i, body, func))


@sign(lambda e: True)
@register
def application(expr, ir):
    operator, operand = expr

    unbound = 0
    while operand:
        e, operand = operand
        compiler(e, ir)
        unbound += 1
    compiler(operator, ir)
    return instruction.apply, (ir, unbound)


def output(expr):
    if expr is not ():
        print(expr)


def evaluator_maker(cont=output):
    ir = []
    env_ = Env()

    def evaluator(expr):
        pc = len(ir)
        env = env_
        values = ()

        if expr is not None:
            compiler(expr, ir)
        ir.append((rtn, ()))
        while True:
            function, arguments = ir[pc]
            # print(pc, values, function)
            if function is rtn and env.parent is None:
                break
            elif function is instruction.self_evaluator:
                pc += 1
                values = (arguments[0], values)
            else:
                env, pc, values = function(env, pc, values, *arguments)
        return cont(values[0])
    return evaluator
