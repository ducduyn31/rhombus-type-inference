from functools import cache
import numpy as np
import pandas as pd

from .base import BaseConvertStrategy
from ..utils import filter_na


class NumericConvertStrategy(BaseConvertStrategy):
    converted = None

    def __init__(self, data, threshold=0.8):
        super().__init__(data, threshold)
        self.data = filter_na(data)

    def is_applicable(self) -> bool:
        t = np.dtype(self.data.dtype).char
        return t in np.typecodes["AllInteger"] + np.typecodes["AllFloat"] or t == "O"

    @cache
    def get_compatibilities(self) -> float:
        df_converted = pd.to_numeric(self.data, errors='coerce')

        if df_converted.isna().all():
            return 0.0

        # Try to make it smallest float possible
        df_converted = pd.to_numeric(df_converted, errors='coerce', downcast='float')

        # If can be converted to integer, do it
        if (df_converted.apply(float.is_integer) | df_converted.isna()).all():
            if df_converted.min() >= 0:
                df_converted = pd.to_numeric(df_converted, errors='coerce', downcast='unsigned')
            else:
                df_converted = pd.to_numeric(df_converted, errors='coerce', downcast='integer')

        invalid_count = df_converted.isna().sum()
        self.converted = df_converted
        return 1 - invalid_count / len(self.data)

    def get_type(self) -> np.dtype:
        return self.convert().dtype

    def convert(self):
        if self.converted is None:
            self.get_compatibilities()
        return self.converted if self.converted is not None else self.data
