#!/bin/env python3
import sys
from ika.struct import Env
from ika.parser import parser
from ika.evaluator import pre_interpreter, eval
from ika.lexer import lexer
from ika.utils import cons_iter

base_env = Env()
base_env = pre_interpreter(base_env)


def run(input_, end=lambda x: sys.stdout.write(repr(x))):
    expr = cons_iter(parser(lexer(input_)))
    for e in expr:
        eval(e, base_env, end=end)


def interactive():
    import readline
    print(";; IKA 0.0.0")
    while True:
        run(input("\n; > "))


def readfile():
    run(sys.stdin.read())


def main():
    if sys.stdin.isatty():
        interactive()
    else:
        readfile()


if __name__ == '__main__':
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        exit()
