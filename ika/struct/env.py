class Env(dict):
    def __init__(self, parent=None):
        self.parent = parent
        self.runtime = {}
