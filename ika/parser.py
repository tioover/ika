from pypeg import Symbol, parse
from .struct.pair import Pair, Empty
class ListContent(Pair): pass
class List(Pair): pass
expr = lambda: [Symbol, List, ]
Empty.grammar = None
List.grammar = '(', ListContent, ')'
ListContent.grammar = [(expr(), ListContent), Empty]


def parser(string):
    return parse(string, expr())
