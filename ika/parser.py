import re
from pypeg import parse, restline
from .struct import Pair, String


class Identifier(str):
    regex = re.compile(r'[\w!@$%^&\.\*_+-=~]+')


class Float(float):
    grammar = re.compile(r'\d+.\d+')


class List:
    def __new__(cls, *args):
        return Pair(*args)


expr = lambda: [Float, int, String, Identifier, Pair]
List.grammar = [
    (expr(), '.', expr()),
    (expr(), List),
    None, ]

String.grammar = '"', re.compile(r'(\\"|[^"])*'), '"'
Pair.grammar = '(', List, ')'


def parser(string):
    return parse(string, expr(), comment=(';', restline))
