from functools import cache

import numpy as np
import pandas as pd

from .base import BaseConvertStrategy
from ..utils import filter_na


class DatetimeConvertStrategy(BaseConvertStrategy):
    converted = None

    def __init__(self, data, threshold=0.8):
        super().__init__(data, threshold)
        self.data = filter_na(data)

    def is_applicable(self) -> bool:
        t = np.dtype(self.data.dtype).char
        test_size = 10
        test_convert_rate = 1 - pd.to_datetime(self.data.head(test_size), errors="coerce").isna().sum() / test_size
        return test_convert_rate >= 0.5 and  (t == np.typecodes["Datetime"] or t == "O")

    @cache
    def get_compatibilities(self) -> float:
        if self.data.dtype == "datetime64":
            return 1.0

        df_converted = pd.to_datetime(self.data, errors="coerce")
        nulls_count = len(self.data[self.data.isna()])
        invalid_count = len(df_converted[df_converted.isna()])
        compat = 1 - invalid_count / len(self.data)

        if compat < self.threshold and invalid_count > nulls_count:
            df_converted = pd.to_datetime(self.data, errors="coerce", dayfirst=True, format="mixed")
            invalid_count = len(df_converted[df_converted.isna()])
            compat = 1 - invalid_count / len(self.data)

        self.converted = df_converted
        return compat

    def get_type(self) -> np.dtype:
        return self.convert().dtype

    def convert(self):
        if self.converted is None:
            self.get_compatibilities()
        return self.converted if self.converted is not None else self.data
