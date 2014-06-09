def id(x):
    return x


def none(*x):
    return None


def true(*x):
    return False


from .struct import Pair, empty


def release(x):
    stack = []
    while True:
        if isinstance(x, Pair):
            if isinstance(x.car, Pair):
                stack.append(x.cdr)
                x = x.car
            else:
                yield x.car
                x = x.cdr
        else:
            if x is not empty:
                yield x
            if stack:
                x = stack.pop()
            else:
                break
