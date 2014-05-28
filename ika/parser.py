from pypeg import Symbol, parse
from .struct.pair import Pair


class ListContent(Pair): pass
class List(Pair): pass
expr = lambda: [Symbol, List, ]
List.grammar = '(', ListContent, ')'
ListContent.grammar = [(expr(), '.', expr()), (expr(), ListContent), None]


def parser(string):
    return parse(string, expr())
