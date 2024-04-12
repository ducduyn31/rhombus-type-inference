from functools import cache

import numpy as np

from .base import BaseConvertStrategy
from ..utils import filter_na


class BooleanConvertStrategy(BaseConvertStrategy):
    TRUTHY_VALUES = ["true", "t", "yes", "y", "1"]
    FALSY_VALUES = ["false", "f", "no", "n", "0", "nan"]
    converted = None

    def __init__(self, data, threshold=0.8):
        super().__init__(data, threshold)
        self.data = filter_na(data)

    def is_applicable(self) -> bool:
        uniques = len(self.data.unique())
        allowed_uniques = len(self.TRUTHY_VALUES) + len(self.FALSY_VALUES) + 3
        t = np.dtype(self.data.dtype).char
        return uniques <= allowed_uniques and (
                    self.data.dtype == "bool" or self.data.dtype == "object" or t in np.typecodes["AllInteger"])

    @cache
    def get_compatibilities(self) -> float:
        if self.data.dtype == "bool":
            return 1.0

        def convert_bool(x):
            if str(x).lower() in self.TRUTHY_VALUES:
                return True
            if str(x).lower() in self.FALSY_VALUES:
                return False
            return np.nan

        df_convert = self.data.apply(convert_bool)
        invalid_count = len(df_convert[df_convert.isna()])
        compat = 1 - invalid_count / len(self.data)
        self.converted = df_convert
        return compat

    def get_type(self):
        return self.convert().dtype

    def convert(self):
        if self.converted is None:
            self.get_compatibilities()
        return self.converted if self.converted is not None else self.data
