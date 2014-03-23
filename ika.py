#!/bin/env python3
import sys
from ika.struct import Env
from ika.parser import parser
from ika.evaluator import eval
from ika.lexer import lexer

base_env = "test"


def run(input_):
    return eval(parser(lexer(input_)), base_env)


def interactive():
    import readline
    print(";; IKA 0.0.0")
    while True:
        print("%s" % run(input("; > ")))


def readfile():
    sys.stdout.write(run(sys.stdin.read()))


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
