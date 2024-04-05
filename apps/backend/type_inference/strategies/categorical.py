from .base import BaseConvertStrategy


class CategoricalConvertStrategy(BaseConvertStrategy):
    def should_convert(self):
        return self.data.dtype == "object"

    def convert(self):
        return self.data.astype("category")
