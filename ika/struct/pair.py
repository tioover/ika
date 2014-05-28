class Pair(tuple):
    @property
    def car(self):
        return self[0]

    @property
    def cdr(self):
        return self[1]


class Empty:
    def __repr__(self):
        return '()'
