import readline
from ika import parser, lexer
p = parser.parser
l = lexer.lexer


def main():
    while True:
        token = l(input())
        print(p(token))


if __name__ == '__main__':
    main()
