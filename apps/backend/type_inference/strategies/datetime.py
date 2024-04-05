from .base import BaseConvertStrategy

class DateTimeConvertStrategy(BaseConvertStrategy):
    def should_convert(self):
        return self.data.dtype == "datetime64"

    def convert(self):
        return self.data.astype("datetime64")