from functools import cache

import numpy as np

from type_inference.strategies.base import BaseConvertStrategy
from type_inference.utils import filter_na


class ComplexNumberConvertStrategy(BaseConvertStrategy):
    converted = None

    def __init__(self, data, threshold=0.8):
        super().__init__(data, threshold)
        self.data = filter_na(data)

    def is_applicable(self) -> bool:
        h = self.data.head()
        while h.isna().all() and len(h) < len(self.data):
            h = self.data.head(len(h) * 2)
        t = np.dtype(h.dtype).char
        return t in np.typecodes["Complex"] or t == "O"

    @cache
    def get_compatibilities(self) -> float:
        if self.data.dtype == "complex":
            return 1.0

        try:
            df_converted = self.data.astype("complex")
            nulls_count = self.data.isna().sum()
            invalid_count = df_converted.isna().sum()
            self.converted = df_converted
            return 1 - invalid_count / (len(self.data) - nulls_count)
        except ValueError:
            return 0.0

    def get_type(self) -> np.dtype:
        return self.convert().dtype

    def convert(self):
        if self.converted is None:
            self.get_compatibilities()
        return self.converted if self.converted is not None else self.data
