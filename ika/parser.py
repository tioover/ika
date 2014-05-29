import re
from pypeg import parse, restline, some
from .struct.types import String, Identifier, Float
from .struct.pair import Empty, Pair, lst


class Number(int):
    pass


class List:
    def __new__(cls, thing):
        tail = thing.pop()
        if not thing:
            return tail
        return lst(*thing, tail=tail)


class Quote:
    def __new__(cls, obj):
        return lst(Identifier('quote'), obj)


class Vector:
    def __new__(cls, obj):
        return Pair(Identifier('vector'), obj)


expr = lambda: [Float, Number, String, Identifier, List, Quote, Vector]

# Grammar Rule
Empty.grammar = None
Identifier.grammar = re.compile(r'[\w!@$%^&\.\*_+-=~]+')
String.grammar = '"', re.compile(r'(\\"|[^"])*'), '"'
Number.grammar = re.compile(r'\d+')
Float.grammar = re.compile(r'\d+\.\d+')
Quote.grammar = "'", expr()
Vector.grammar = '#', List
list_content = [
    (some(expr()),  # list item
        [('.', expr()), Empty]),  # tail item
    Empty, ]
List.grammar = [
    ('(', list_content, ')'),
    ('[', list_content, ']'),
    ('{', list_content, '}'), ]


def parser(string):
    return parse(string, expr(), comment=(';', restline))
