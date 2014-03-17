#!/bin/env python3
import sys


def repl():
    run = lambda string: string
    if sys.stdin.isatty():
        line = 1
        import readline
        print(";; IKA 0.0.0")
        while True:
            print(">> %s" % run(input()))
            line += 1
    else:
        sys.stdout.write(run(sys.stdin.read()))

if __name__ == '__main__':
    repl()
