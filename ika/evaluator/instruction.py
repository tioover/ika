from ika.evaluator import rtn, Env
from ika.struct import Identifier, Pair
from ika.struct.types import Cont
from ika.utils import release


def name(env, pc, values, expr):
    return env, pc + 1, (env[expr], values)


def self_evaluator(env, pc, values, expr):
    return env, pc + 1, (expr, values)


def define_empty(env, pc, values, key):
    env[key] = ()
    return env, pc + 1, values


def set_value(env, pc, values, key):
    v, values = values
    env.set_ref(key, v)
    return env, pc + 1, ((), values)


def begin(env, pc, values, num):
    v, values = values
    num -= 1
    for i in range(num):
        values = values[1]
    return env, pc + 1, (v, values)


def callcc(env, pc, values):
    return env, pc + 1, (Cont(values), values)


def lambda_(env, pc, values, next_pc, body, func):
    for atom in release(body):
        if isinstance(atom, Identifier):
            ref = env.get_ref(atom)
            if ref is not None:
                func.closure[atom] = ref
    return env, next_pc, (func, values)


def bound(env, formal, actual):
    while isinstance(formal, Pair):
        key, formal = formal
        value, actual = actual
        env[key] = value
    if formal is not ():
        env[formal] = actual


def apply(env, pc, values, ir, unbound):
    pc += 1
    func, values = values

    # cont jump.
    if isinstance(func, Cont):
        value, values = values
        return func.env, func.pc, (value, func.values)

    args = ()
    for i in range(unbound):
        arg, values = values
        args = Pair((arg, args))

    # call/cc
    if args is not () and isinstance(args[0], Cont):
        cont = args[0]
        cont.pc = pc
        cont.env = env
        cont.values = values

    is_tail_call = pc < len(ir) and (
        env.parent is not None) and (
            ir[pc][0] is begin) and (
                ir[pc + 1][0] is rtn)
    if not is_tail_call:
        env = Env(env)
        env.rtn = (pc, values)
    env.data = func.closure.copy()
    bound(env, func.args, args)
    return env, func.pc, ()
