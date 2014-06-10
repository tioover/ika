from ika.evaluator import rtn, Status
from ika.struct import empty, Identifier, Pair
from ika.struct.types import Cont
from ika.utils import release


def normal(f):
    def instruction(st, pc, *args):
        st.values.append(f(st, pc, *args))
        return st, pc+1
    return instruction


@normal
def name(st, pc, expr):
    return st[expr]


@normal
def self_evaluator(st, pc, expr):
    return expr


@normal
def define(st, pc, key):
    st[key] = st()
    return empty


@normal
def set_value(st, pc, key):
    value = st()
    st.set_ref(key, value)
    return empty


@normal
def begin(st, pc, num):
    value = st()
    num -= 1
    for i in range(num):
        st()
    return value


@normal
def callcc(st, pc):
    return Cont()


def lambda_(st, pc, next_pc, body, func):
    for atom in release(body):
        if isinstance(atom, Identifier):
            ref = st.get_ref(atom)
            if ref is not None:
                func.closure[atom] = ref

    st.values.append(func)
    return st, next_pc


def bound(env, formal, actual):
    while isinstance(formal, Pair):
        env[formal.car] = actual.car
        formal = formal.cdr
        actual = actual.cdr
    if formal is not empty:
        env[formal] = actual


def apply(st, pc, ir, unbound, apply_with_cont=False):
    pc += 1
    func = st()

    # cont jump.
    if isinstance(func, Cont):
        value = st()
        st.values.clear()
        func.st.values.append(value)
        return func.st, func.pc

    args = empty
    for i in range(unbound):
        args = Pair(st(), args)

    # call/cc
    if apply_with_cont:
        cont = args.car
        cont.pc = pc
        cont.st = st

    if pc < len(ir) and ir[pc][0] is rtn:  # tail call
        st.values.clear()
    else:
        st = Status(st)
        st.rtn = pc

    st.env = func.closure.copy()
    bound(st, func.args, args)
    return st, func.pc
