from ika.parser import parser
from ika.evaluator import evaluator


def main():
    import readline
    print(';; ika 1*10^-42')
    eval_ = evaluator()
    while True:
        eval_(parser(input('; >> ')))

if __name__ == '__main__':
    main()
