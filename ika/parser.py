from .struct import Pair
from .const import quote, replace


def parser(lexed, i=0, end=False):
    while i < len(lexed):
        token = lexed[i]
        if token in replace:
            lexed[i: i+1] = replace[token]
            token = lexed[i]

        if token == '(':  # TODO ")" banlance
            head = None
            # Push stack.
            for pair, i in parser(lexed, i+1):
                if head is None:
                    head = pair
                    prev = head
                else:
                    prev.cdr = pair
                    prev = prev.cdr
            yield Pair(head), i+1

        elif token == ')':
            if end:  # Stack empty, can't pop.
                raise SyntaxError("Brackets \")\" do not match pair.")
            # Pop stack.
            break

        elif token == '.':
            yield lexed[i+1], i+1
            break

        elif token in quote:
            gen = parser(lexed, i+1)
            expr, i = next(gen)
            expr = Pair(quote[token], expr)
            yield Pair(expr), i

        else:
            yield Pair(token), i

        i += 1
