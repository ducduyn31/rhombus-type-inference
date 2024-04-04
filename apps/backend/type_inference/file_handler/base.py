class BaseFileHandler:
    source: str

    def handle(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")