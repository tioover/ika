class Symbol():

    def __init__(self, string):
        self._string = string

    def __str__(self):
        return self._string


from .utils import Singleton


class T(Singleton):
    pass


class F(Singleton):
    pass


class Nil(Singleton):
    pass


t = T()
f = F()
nil = Nil()
