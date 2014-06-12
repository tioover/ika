from ika.parser import parser
from ika.evaluator import evaluator


def main():
    import readline
    print(';; ika 1*10^-42')
    eval_ = evaluator()
    while True:
        for expr in parser(input('; >> ')):
            eval_(expr)

if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        exit()
