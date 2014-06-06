import unittest
import logging
from ika.parser import parser
from ika.evaluator import Status, compiler
from ika.utils import id


class InterpreterTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.st = Status()
        super(InterpreterTestCase, self).__init__(*args, **kwargs)

    def eval(self, expr):
        return compiler(parser(expr))(self.st, id)

    def log(self, expr):
        logging.info(self.eval(expr))

    def test_lambda(self):
        self.log('(lambda (a b c) a)')
        self.log('((lambda (a b c) b) 1 2 3)')
        self.log('((lambda (a b c) (a b c)) (lambda (a b) a) 1 2)')

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
