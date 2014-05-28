import unittest
from ika.parser import parser


log = lambda s: print(repr(parser(s)))
logall = lambda *l: list(map(log, l))


class ParserTestCase(unittest.TestCase):
    def test_list(self):
        logall(
            '(1 2 3 4 5)',
            '()',
            '((1 2 3) 4 5 6)',
            '(1 2 3 (4 5 6))',
            '(1 2 (3 4 5 6) 7 8)',
            '((1 (2 (3 (4)))))',
        )

    def test_pair(self):
        logall(
            '(1 . 2)',
            '(1 2 . 3)',
        )

    def test_type(self):
        log('(1 a 1.1)')

    def test_comment(self):
        log('42 ;test')


class InterpreterTestCase(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
