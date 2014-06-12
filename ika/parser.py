import re
from pypeg import parse, restline, some, omit
from .struct import String, Identifier, Number, Float, Pair, Empty, empty


class List:
    def __new__(cls, thing):
        tail = thing.pop()
        if not thing:
            return tail
        while thing:
            tail = Pair(thing.pop(), tail)
        return tail


class Quote:
    def __new__(cls, obj):
        if obj is empty:
            return empty
        return Pair('quote', Pair(obj))


class Vector:
    def __new__(cls, obj):
        return Pair(Identifier('vector'), obj)


expr = lambda: [Float, Number, String, Identifier, List, Quote, Vector]


# Grammar Rule
Empty.grammar = None
Identifier.grammar = re.compile(r'(?!\d|\.\s)[\w!@$%^&\.\*_+-=~]+')
String.grammar = '"', re.compile(r'(\\"|[^"])*'), '"'
Number.grammar = re.compile(r'\d+')
Float.grammar = re.compile(r'\d+\.\d+')
Quote.grammar = "'", expr()
Vector.grammar = '#', List
list_content = [
    (some(expr()),  # list item
        [(omit('.'), expr()), Empty]),  # tail item
    Empty, ]
List.grammar = [
    ('(', list_content, ')'),
    ('[', list_content, ']'),
    ('{', list_content, '}'), ]


def parser(string):
    return parse(string, [some(expr()), re.compile(r'\s*')], comment=(';', restline))
