#!/bin/env python3
import sys
from ika.const import base_scm
from ika.struct import Env
from ika.parser import parser
from ika.evaluator import eval_
from ika.lexer import lexer


def pre_interpreter(base_env):
    with open(base_scm) as src:
        for expr in parser(lexer(src.read()), pre=True):
            eval_(expr, base_env)
    return base_env

base_env = Env()
base_env = pre_interpreter(base_env)


def run(input_, end=None):
    for e in parser(lexer(input_)):
        eval_(e, base_env, end=end)


def interactive():
    import readline
    print(";; IKA 0.0.1")
    while True:
        run(input("; > "), lambda x: print(repr(x)))


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
