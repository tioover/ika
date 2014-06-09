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
        st[name] = st()
        return empty
    return define


@sign(car_is('set!'))
@register
def assign(expr, ir):
    k = expr.cdr.car
    v = expr.cdr.cdr.car
    compile(v, ir)

    @normal
    def set(st, pc):
        v = st()
        st.setref(k, v)
        return empty
    return set


@sign(car_is('begin'))
@register
def begin(expr, ir):
    expr = expr.cdr
    n = 0
    for e in expr:
        compile(e, ir)
        n += 1

    @normal
    def getlast(st, pc):
        v = st()
        i = n - 1
        for j in range(i):
            st()
        return v
    return getlast


@sign(car_is('lambda'))
def _lambda(expr, ir):
    pc = len(ir)
    ir.append(None)  # Placeholder

    args = expr.cdr.car
    body = expr.cdr.cdr
    func = Function(args, pc+1)

    compile(Pair('begin', body), ir)
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
        func = st()
        args = empty
        for i in range(unbound):
            args = Pair(st(), args)
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
