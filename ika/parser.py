from .struct import Pair, empty
# from .utils import cons_convert
from functools import reduce

transfrom = {
    "'(": "quote",
    "`(": "quasiquote",
    ",@(": "unquote-splicing",
    ',(': "unquote",
    "#(": "vector",
}


def convert_tree(lexed, i=0, end=False):
    '''
    lexed : List from lexer.
    i : Position cursor for lexed.
    end : A flag, if True, stack is empty.
    '''
    tree = []

    while i < len(lexed):
        token = lexed[i]
        if token == '(':
            # Push stack.
            subtree, i = convert_tree(lexed, i+1)
            tree.append(subtree)
        elif token == ')':
            if end:  # Stack empty, can't pop.
                raise SyntaxError("Brackets \")\" do not match pair.")
            # Pop stack.
            return tree, i
        elif token in transfrom:
            subtree, i = convert_tree(lexed, i+1)
            tree.append([transfrom[token], subtree])
            # TODO: (a . b) (a b . c) (lambda (a . b)(..))
        else:
            tree.append(token)
        i += 1

    if not end:  # Stack not empty.
        raise SyntaxError("Brackets \"(\" do not match pair.")
    return tree


def convert_s_exp(tree):
    ''' Recursion convert Python list to Lisp list'''
    head = Pair(None, empty)

    def f(pair, elem):
        if type(elem) is list:
            elem = convert_s_exp(elem)
        pair.cdr = Pair(elem, empty)
        return pair.cdr
    reduce(f, tree, head)
    return head.cdr


def parser(lexed):
    tree = convert_tree(lexed, end=True)
    return convert_s_exp(tree)
