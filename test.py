import unittest
from ika.parser import parser


class ParserTestCase(unittest.TestCase):
    def test_atom(self):
        print(parser('a'))

    def test_list(self):
        print(parser('(1 2 3 4 5)'))
        print(parser('()'))
        print(parser('((1 2 3) 4 5 6)'))
        print(parser('(1 2 3 (4 5 6))'))
        print(parser('(1 2 (3 4 5 6) 7 8)'))
        print(parser('((1 (2 (3 (4)))))'))
        print(parser('(1 2 3 4 . 5)'))


class InterpreterTestCase(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
