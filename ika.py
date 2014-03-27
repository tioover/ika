#!/bin/env python3
import sys
from ika.struct import Env
from ika.parser import parser
from ika.evaluator import pre_interpreter, eval_
from ika.lexer import lexer

base_env = Env()
base_env = pre_interpreter(base_env)


def run(input_, end=lambda x: sys.stdout.write(repr(x))):
    for e in parser(lexer(input_)):
        eval_(e, base_env, end=end)


def interactive():
    import readline
    print(";; IKA 0.0.1")
    while True:
        run(input("\n; > "))


def readfile():
    run(sys.stdin.read(), lambda x: x)


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
