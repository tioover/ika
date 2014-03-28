from .struct import Pair, empty, pyapply_flag
from .const import quote, lex_replace


def expr_gen(lexed, i=0, pre=False):
    while i < len(lexed):
        token = lexed[i]
        if token in lex_replace:
            lexed[i: i+1] = lex_replace[token]
            continue

        if token == '(':
            i += 1  # skip '('
            gen = expr_gen(lexed, i, pre)
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

        elif token == "()":
            yield Pair(empty), i

        elif pre and token == "pyapply":
            yield Pair(pyapply_flag), i

        elif token in quote:
            gen = expr_gen(lexed, i+1, pre)
            expr, i = next(gen)
            expr = Pair(quote[token], expr)
            yield Pair(expr), i

        else:
            yield Pair(token), i

        i += 1


def parser(lexed, pre=False):
    if not lexed:
        return empty

    head = Pair(None)
    prev = head

    for now, i in expr_gen(lexed, pre=pre):
        prev.cdr = now
        prev = now
    if i >= len(lexed):
        raise SyntaxError("Unexpected '('")
    elif i+1 < len(lexed):
        raise SyntaxError("Unexpected ')'")
    return head.cdr
