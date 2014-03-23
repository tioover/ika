#!/bin/env python3
import sys
from config import config
from struct import Env
from parser import parser
from evaluator import eval
from lexer import lexer

base_env = Env()


def run(input_):
    return eval(parser(lexer(input_)), base_env)


def interactive():
    readline.read_history_file([config["history_path"]])
    print(";; IKA 0.0.0")
    while True:
        print("%s" % run(input("; >")))


def readfile():
    sys.stdout.write(run(sys.stdin.read()))


if __name__ == '__main__':
    if sys.stdin.isatty():
        import readline
        try:
            interactive()
        except KeyboardInterrupt:
            readline.read_history_file([config["history_path"]])
            exit()
    else:
        try:
            readfile()
        except EOFError:
            exit()
