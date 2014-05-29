class Float(float):
    pass


class String(str):
    def __repr__(self):
        return '"%s"' % self


class Identifier(str):
    def __repr__(self):
        return self


class Quote:
    pass
