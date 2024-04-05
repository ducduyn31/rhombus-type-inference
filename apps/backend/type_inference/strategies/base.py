class BaseConvertStrategy:

    def __init__(self, data):
        self.data = data

    def should_convert(self):
        raise NotImplementedError

    def convert(self):
        raise NotImplementedError
