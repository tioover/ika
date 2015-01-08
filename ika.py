from ika.parser import parser
from ika.evaluator import evaluator_maker


def main():
    import readline
    print(';; ika 1*10^-42')
    evaluator = evaluator_maker()
    while True:
        for expr in parser(input('; >> ')):
            evaluator(expr)

if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        exit()
