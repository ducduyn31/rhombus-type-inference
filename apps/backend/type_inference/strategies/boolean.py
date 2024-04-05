from .base import BaseConvertStrategy


class BooleanConvertStrategy(BaseConvertStrategy):
    def should_convert(self):
        return self.data.dtype == "bool"

    def convert(self):
        return self.data.astype("bool")
