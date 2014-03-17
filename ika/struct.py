class Symbol():

    def __init__(self, string):
        self._string = string

    def __str__(self):
        return self._string


class T():
    pass


class F():
    pass


class Nil():
    pass

t = T()
f = F()
nil = Nil()
