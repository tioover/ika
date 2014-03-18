from .struct import Pair
from .const import transfrom, TEMP


def convert_tree(lexed, i=0, end=False):
    '''
    lexed : List from lexer.
    i : Position cursor for lexed.
    end : A flag, if True, stack is empty.
    return value : head of pair list.
    '''
    prev = TEMP  # a temp pair, simpily program struct.

    while i < len(lexed):
        token = lexed[i]

        if token == '(':
            # Push stack.
            subtree, i = convert_tree(lexed, i+1)
            prev.append(subtree)

        elif token == ')':
            if end:  # Stack empty, can't pop.
                raise SyntaxError("Brackets \")\" do not match pair.")
            # Pop stack.
            return TEMP.cdr, i

        elif token in transfrom:
            subtree, i = convert_tree(lexed, i+1)
            prev.append(Pair(transfrom[token], Pair(subtree)))
        elif token == '.':
            i += 1
            prev.cdr = lexed[i]
        else:
            prev.append(token)
        prev = prev.cdr
        i += 1

    if not end:  # Stack not empty.
        raise SyntaxError("Brackets \"(\" do not match pair.")
    return TEMP.cdr


def parser(lexed):
    exp = convert_tree(lexed, end=True)
    return exp
