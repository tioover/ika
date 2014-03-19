from .struct import Pair
from .const import quote, replace


def expr_gen(lexed, i=0):
    while i < len(lexed):
        token = lexed[i]
        if token in replace:
            lexed[i: i+1] = replace[token]
            continue

        if token == '(':
            i += 1  # skip '('
            gen = expr_gen(lexed, i)
            head, i = next(gen)
            prev = head
            for pair, i in gen:
                prev.cdr = pair
                prev = prev.cdr
            i += 1  # skip ')'
            yield Pair(head), i

        elif token == ')':
            # Pop stack.
            break

        elif token == '.':
            i += 1  # skip '.'
            yield lexed[i], i
            break

        elif token in quote:
            gen = expr_gen(lexed, i+1)
            expr, i = next(gen)
            expr = Pair(quote[token], expr)
            yield Pair(expr), i

        else:
            yield Pair(token), i

        i += 1


def parser(lexed):
    gen = expr_gen(lexed)
    head, i = next(gen)
    try:
        for expr, i in gen:
            head.cdr = expr
    except AttributeError:
        raise SyntaxError("Unexpected '('")
    if i >= len(lexed):
        raise SyntaxError("Unexpected '('")
    elif i+1 < len(lexed):
        raise SyntaxError("Unexpected ')'")
    return head
