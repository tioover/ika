import unittest
import logging
from ika.parser import parser
from ika.evaluator import Status, compiler
from ika.struct import Function
from ika.utils import id


class InterpreterTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.st = Status()
        self.ir = []
        super(InterpreterTestCase, self).__init__(*args, **kwargs)

    def eval(self, expr):
        return compiler(self.ir, parser(expr))(self.st, id)

    def log(self, str):
        logging.info(str)

    def test_lambda(self):
        assert isinstance(self.eval('(lambda (a b c) a)'), Function)

    def test_apply(self):
        assert self.eval('((lambda (x) x) 42)') == 42
        assert self.eval('((lambda (a b c) b) 1 2 3)') == 2
        assert self.eval('((lambda (a b c) (a b c)) (lambda (a b) a) 42 43)') == 42
        assert self.eval('((lambda a a) 1 2 3)').car == 1

    def test_closure(self):
        assert self.eval('(((lambda (x) (lambda () 42)) 42))') == 42

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
