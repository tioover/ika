from ..struct import Pair, Procedure
from ..utils import get_operand, get_operator


def condition(expr):
    return isinstance(expr, Pair)


def analyze(analyzer, expr):

    def analyzed(env):
        operator = analyzer(get_operator(expr))(env)
        operand = map(lambda e: analyzer(e)(env), get_operand(expr))
        if not isinstance(operator, Procedure):
            raise TypeError("%s is not procedure." % str(operator))
        new_env = env.extend(dict(zip(operator.formal_args, operand)))
        return operator.body(new_env)

    return analyzed
