def match():
    pipeline = []
    register = lambda *x: pipeline.append(x)

    def handing(*args, **kwargs):
        for cond, handler in pipeline:
            if cond(*args, **kwargs):
                return handler(*args, **kwargs)
    return register, handing


def id(x):
    return x


def none(x):
    return None


def consmap(f, lst):
    for i in lst:
        yield f(i)
