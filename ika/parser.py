import re
from pypeg import parse, restline, some, omit
from .struct import String, Identifier, Number, Float, Pair, IkaType


class Empty:
    def __new__(cls):
        return ()


class List:
    def __new__(cls, li):
        tail = li.pop()
        if not li:
            return tail
        while li:
            tail = Pair((li.pop(), tail))
        return tail


class Quote:
    def __new__(cls, x: IkaType):
        if x is ():
            return ()
        return Pair((Identifier('quote'), x))


class Vector:
    def __new__(cls, x: IkaType):
        return Pair((Identifier('vector'), x))


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


def parser(string) -> IkaType:
    return parse(string, [some(expr()), re.compile(r'\s*')], comment=(';', restline))
