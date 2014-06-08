from ..struct import Pair, empty, Identifier, Function
from .backend import Status, sign, register, normal,\
    car_is, compile, compiler, rtn


@sign(lambda e: isinstance(e, Identifier))
@register
def name(expr, ir):
    @normal
    def obj(st, pc):
        while st is not None:
            if expr in st.env:
                return st.env[expr]
            st = st.parent
    return obj


@sign(lambda e: not isinstance(e, Pair))
@register
def self_evaluator(expr, ir):
    @normal
    def obj(st, pc):
        return expr
    return obj


@sign(car_is('define'))
@register
def definition(expr, ir):
    name = expr.cdr.car
    value = expr.cdr.cdr.car
    compile(value, ir)

    @normal
    def define(st, pc):
        st.env[name] = st.values.pop()
        return empty
    return define


@sign(car_is('lambda', '\\', 'λ'))
def _lambda(expr, ir):
    pc = len(ir)
    ir.append(None)  # Placeholder

    args = expr.cdr.car
    body = expr.cdr.cdr.car
    func = Function(args, pc+1)

    compile(body, ir)
    ir.append(rtn)
    i = len(ir)  # skip function body.

    def function_obj(st, pc):
        func.env = st.env
        st.values.append(func)
        return st, i

    ir[pc] = function_obj


def args_bind(env, formal, actual):
    while True:
        if isinstance(formal, Pair):
            env[formal.car] = actual.car
            formal = formal.cdr
            actual = actual.cdr
        elif formal is empty:
            break
        else:
            env[formal] = actual


@sign(lambda e: True)
def application(expr, ir):
    operator = expr.car
    operand = expr.cdr

    i = -1
    for i, e in enumerate(operand):
        compile(e, ir)
    compile(operator, ir)

    def apply(st, pc):
        func = st.values.pop()
        args = empty
        for j in range(i+1):
            args = Pair(st.values.pop(), args)
        nextpc = pc + 1
        if nextpc < len(ir) and ir[nextpc] is rtn:  # tail call
            nextpc = st.rtn
        else:
            st = Status(st)
            st.rtn = pc+1
        st.env = func.env
        args_bind(st.env, func.args, args)
        return st, func.pc

    ir.append(apply)


def eval(expr, ir, st, cont=print):
    return compiler(ir, expr)(st, cont)
