import readline
from ika import parser, lexer
p = parser.parser
l = lexer.lexer


def parser():
    while True:
        for exp, i in p(l(input())):
            print(exp.car)


if __name__ == '__main__':
    parser()
