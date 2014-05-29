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
            '((k (h (i (j)))))',
        )

    def test_pair(self):
        logall(
            '(1 . 2)',
            '(1 2 . 3)',
        )

    def test_type(self):
        def t(s, r):
            assert parser(s) == r
        t('abc', 'abc')
        t('123', 123)
        t('1.23', 1.23)
        t('"helo \\" world\\n"', 'helo \\" world\\n')

    def test_comment(self):
        log('(42 "test") ;test')

    def test_quote(self):
        log("'(1 2 3)")
        log("'aaa")
        log("'()")

    def test_vector(self):
        log('#(1 2 3 4)')


class InterpreterTestCase(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
