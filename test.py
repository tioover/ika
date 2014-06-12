import unittest
import logging
from ika.parser import parser
from ika.evaluator import evaluator
from ika.struct import Function, empty
from ika.utils import id


eval_ = evaluator(id)


def e(string):
    v = None
    for expr in parser(string):
        v = eval_(expr)
    return v


class InterpreterTestCase(unittest.TestCase):
    def log(self, string):
        logging.info(string)

    def test_lambda(self):
        assert isinstance(e('(lambda (a b c) a)'), Function)

    def test_apply(self):
        assert e('((lambda (x) x) 42)') == 42
        assert e('((lambda (a b c) b) 1 2 3)') == 2
        assert e('((lambda (a b c) (a b c)) (lambda (a b) a) 42 43)') == 42
        assert e('((lambda a a) 1 2 3)').car == 1

    def test_closure(self):
        assert e('(((lambda (x) (lambda () 42)) 42))') == 42

    def test_callcc(self):
        e('''
        (define a 0)
        (define b 0)
        (set! a (call/cc (lambda (cc) (set! b cc))))
        ''')
        assert e('a') is empty
        e('(b 42)')
        assert e('a') == 42

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
