import unittest
import logging
from ika.parser import parser
from ika.evaluator import evaluator
from ika.struct import Function, empty
from ika.utils import id


eval_ = evaluator(id)


class InterpreterTestCase(unittest.TestCase):
    def eval(self, expr):
        return eval_(parser(expr))

    def log(self, string):
        logging.info(string)

    def test_lambda(self):
        assert isinstance(self.eval('(lambda (a b c) a)'), Function)

    def test_apply(self):
        assert self.eval('((lambda (x) x) 42)') == 42
        assert self.eval('((lambda (a b c) b) 1 2 3)') == 2
        assert self.eval('((lambda (a b c) (a b c)) (lambda (a b) a) 42 43)') == 42
        assert self.eval('((lambda a a) 1 2 3)').car == 1

    def test_closure(self):
        assert self.eval('(((lambda (x) (lambda () 42)) 42))') == 42

    def test_callcc(self):
        self.eval('(define a 0)')
        self.eval('(define b 0)')
        self.eval('(set! a (call/cc (lambda (cc) (set! b cc))))')
        assert self.eval('a') is empty
        self.eval('(b 42)')
        assert self.eval('a') == 42

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
