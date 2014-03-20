from ..utils import get_module_name

modules = []
pipeline = []

for name in get_module_name(__path__[0]):
    __import__("%s.%s" % (__name__, name))
    module = eval(name)
    modules.append(module)
    pipeline.append((module.condition, module.analyze))


def analyzer(expr):
    for condition, analyze in pipeline:
        if condition(expr):
            return analyze(analyzer, expr)
