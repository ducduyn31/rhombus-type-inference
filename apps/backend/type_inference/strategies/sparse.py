from .base import BaseConvertStrategy


class SparseConvertStrategy(BaseConvertStrategy):
    def should_convert(self):
        return self.data.dtype == "object"

    def convert(self):
        return self.data.astype("Sparse")
