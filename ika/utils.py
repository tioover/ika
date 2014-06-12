def id(x):
    return x


def none(*x):
    return None


def true(*x):
    return False


from .struct import Pair


def release(x):
    stack = []
    while True:
        if isinstance(x, Pair):
            car, cdr = x
            if isinstance(car, Pair):
                stack.append(cdr)
                x = car
            else:
                yield car
                x = cdr
        else:
            if x is not ():
                yield x
            if stack:
                x = stack.pop()
            else:
                break
