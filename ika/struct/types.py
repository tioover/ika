class Float(float):
    pass


class Number(int):
    pass


class String(str):
    def __repr__(self):
        return '"%s"' % self


class Identifier(str):
    def __repr__(self):
        return self


class Quote:
    pass


class Function:
    def __init__(self, args, pc):
        self.args = args
        self.pc = pc
        self.closure = {}
