class IkaType:
    pass


class Float(IkaType, float):
    pass


class Number(IkaType, int):
    pass


class String(IkaType, str):
    def __repr__(self):
        return '"%s"' % self


class Identifier(IkaType, str):
    def __repr__(self):
        return self


class Quote:
    pass


class Function(IkaType):
    def __init__(self, args, pc):
        self.args = args
        self.pc = pc
        self.closure = {}


class Cont(Function):
    def __init__(self, values):
        self.args = None
        self.values = values
        self.env = None
        self.pc = None
