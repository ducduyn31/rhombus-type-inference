from functools import cache

import pandas as pd

from .base import BaseConvertStrategy
from ..utils import filter_na


class CategoricalConvertStrategy(BaseConvertStrategy):
    converted = None

    def __init__(self, data, threshold=0.8):
        super().__init__(data, threshold)
        self.data = filter_na(data)

    def is_applicable(self) -> bool:
        if len(self.data.unique()) > 50:
            return False
        try:
            pd.to_datetime(self.data)
            return False
        except:
            return self.data.dtype == "object" and len(self.data.unique()) / len(self.data) < self.threshold

    def should_convert(self) -> (float, bool):
        rows = len(self.data)
        unique = len(self.data.unique())
        return unique / rows, 1 - unique / rows >= self.threshold

    @cache
    def get_compatibilities(self) -> float:
        if self.data.dtype == "category":
            return 1.0

        rate, should_convert = self.should_convert()

        if should_convert:
            df_converted = pd.Categorical(self.data)
            self.converted = df_converted

        return 1 - rate

    def get_type(self):
        return self.convert().dtype

    def convert(self):
        if self.converted is not None:
            self.get_compatibilities()
        return self.converted if self.converted is not None else self.data
