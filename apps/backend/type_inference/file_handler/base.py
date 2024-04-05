class BaseFileHandler:
    
    def __init__(self, source):
        self.source = source

    def handle(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")
