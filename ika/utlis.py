class Framework:
    tested = None

    def __init__(self, pipline=None):
        if pipline is None:
            pipline = []
        self.pipline = pipline

    def __call__(self, *args, **kwargs):
        for cond, handler in self.pipline:
            if cond(self, *args, **kwargs):
                return handler(self, *args, **kwargs)

    def add(self, cond, handler):
        self.pipline.append((cond, handler))

    def sign(self, cond):
        def wrap(handler):
            self.add(cond, handler)
            return handler
