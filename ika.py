'''REPL'''
from ika.parser import parser
from ika.evaluator import Status, eval


def main():
    import readline
    print(';; ika 1*10^-42')
    st = Status()
    ir = []
    while True:
        eval(parser(input('; >> ')), ir, st)

if __name__ == '__main__':
    main()
