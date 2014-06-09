from ..struct import Pair, empty, Identifier, Function
from .backend import Status, sign, register, normal,\
    car_is, compile, compiler, rtn
from ..utils import release


@sign(lambda e: isinstance(e, Identifier))
@register
def name(expr, ir):
    @normal
    def obj(st, pc):
        return st[expr]
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
        st[name] = st.values.pop()
        return empty
    return define


@sign(car_is('lambda'))
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
        for atom in release(body):
            if isinstance(atom, Identifier):
                ref = st.getref(atom)
                if ref is not None:
                    func.closure[atom] = ref

        st.values.append(func)
        return st, i

    ir[pc] = function_obj


def bound(env, formal, actual):
    while isinstance(formal, Pair):
        env[formal.car] = actual.car
        formal = formal.cdr
        actual = actual.cdr
    if formal is not empty:
        env[formal] = actual


@sign(lambda e: True)
def application(expr, ir):
    operator = expr.car
    operand = expr.cdr

    unbound = 0
    for e in operand:
        compile(e, ir)
        unbound += 1
    compile(operator, ir)

    def apply(st, pc):
        pc += 1
        func = st.values.pop()
        args = empty
        for i in range(unbound):
            args = Pair(st.values.pop(), args)
        if pc < len(ir) and ir[pc] is rtn:  # tail call
            st.values.clear()
        else:
            st = Status(st)
            st.rtn = pc

        st.env = func.closure.copy()
        bound(st, func.args, args)
        return st, func.pc

    ir.append(apply)


def eval(expr, ir, st, cont=print):
    return compiler(ir, expr)(st, cont)
