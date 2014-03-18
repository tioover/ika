from .struct import Pair
from .const import quote, replace


def convert_tree(lexed, cursor=0, end=False):
    '''
    lexed :
        List from lexer.
    cursor :
        Position cursor for lexed.
    end :
        A flag, if True, stack is empty.
    return value :
        head of pair list.
    '''
    head = Pair(None)  # a temp pair, simpily program struct.
    prev = head

    while cursor < len(lexed):
        token = lexed[cursor]

        if token in replace:
            replace_list = replace[token]
            lexed[cursor: cursor+1] = replace_list
            token = lexed[cursor]

        if token == '(':
            # Push stack.
            subtree, cursor = convert_tree(lexed, cursor+1)
            prev.append(subtree)

        elif token == ')':
            if end:  # Stack empty, can't pop.
                raise SyntaxError("Brackets \")\" do not match pair.")
            # Pop stack.
            return head.cdr, cursor

        elif token in quote:
            content = None
            if lexed[cursor+1] == '(':
                content, cursor = convert_tree(lexed, cursor+2)
                content = Pair(content)
            else:
                cursor += 1
                content = lexed[cursor]
            prev.append(Pair(quote[token], content))

        elif token == '.':
            cursor += 1
            prev.cdr = lexed[cursor]

        else:
            prev.append(token)

        prev = prev.cdr
        cursor += 1

    if not end:  # Stack not empty.
        raise SyntaxError("Brackets \"(\" do not match pair.")
    return head.cdr


def parser(lexed):
    exp = convert_tree(lexed, end=True)
    return exp
