import readline
from ika import parser, lexer
p = parser.parser
l = lexer.lexer


def main():
    while True:
        token = l(input())
        print(token)
        # for exp, i in p(token):
        #     print(repr(exp.car))


if __name__ == '__main__':
    main()
