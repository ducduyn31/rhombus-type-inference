from .base import BaseConvertStrategy
class NumericConvertStrategy(BaseConvertStrategy):
    def should_convert(self):
        return self.data.dtype == "int64" or self.data.dtype == "float64"

    def convert(self):
        return self.data.astype("float64")