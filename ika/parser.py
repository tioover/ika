import re
from pypeg import parse, blank, restline
from .struct import Pair


class Id(str):
    regex = re.compile('[\w!@$%^&*_+-=~]+')


class Number(int):
    regex = re.compile('\d\S+')


class List(Pair):
    pass

expr = lambda: [Number, Id, Pair, ]
Pair.grammar = '(', List, ')'
List.grammar = [
    (expr(), blank, '.', blank, expr()),
    (expr(), List),
    None,
]


def parser(string):
    return parse(string, expr(), comment=(';', restline))
