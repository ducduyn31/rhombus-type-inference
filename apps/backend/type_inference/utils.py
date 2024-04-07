import pandas as pd
import numpy as np

def filter_na(value: pd.Series) -> pd.Series:
    #TODO: Convert to vector using BERT or Word2Vec to compare meaning of strings
    strs_null_values = ["not available", "n/a", "na", "nan", "none", "null", "missing", "not found"]
    nulls_value = [np.nan]

    nulls_index = value.apply(lambda x: x.lower() if isinstance(x, str) else x).isin(strs_null_values + nulls_value)
    return value.where(~nulls_index, np.nan)