import re
from pypeg import parse, restline
from .struct import Pair, String
from .struct.pair import lst


class Identifier(str):
    regex = re.compile(r'[\w!@$%^&\.\*_+-=~]+')

    def __repr__(self):
        return self


class Float(float):
    grammar = re.compile(r'\d+.\d+')


class List:
    def __new__(cls, *args):
        return Pair(*args)


class Quote:
    def __new__(cls, obj):
        return lst(Identifier('quote'), obj)

expr = lambda: [Float, int, String, Identifier, Pair, Quote]
Quote.grammar = "'", expr()
List.grammar = [
    (expr(), '.', expr()),
    (expr(), List),
    None, ]

String.grammar = '"', re.compile(r'(\\"|[^"])*'), '"'
Pair.grammar = '(', List, ')'


def parser(string):
    return parse(string, expr(), comment=(';', restline))
