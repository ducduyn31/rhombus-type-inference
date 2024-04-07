import numpy as np
import pandas as pd

from type_inference.strategies import ALL_STRATEGIES


def infer_type_of_col(col: pd.Series, threshold = 0.8) -> np.dtype:
    threshold = get_suggested_threshold(col) if threshold == "auto"  else threshold
    strategies = map(lambda x: x(data=col, threshold=threshold), ALL_STRATEGIES)
    candidates = []
    for strategy in strategies:
        try:
            if strategy.is_applicable() and strategy.get_compatibilities() >= threshold:
                candidates.append(strategy)
                #TODO: At the moment we just assume that the first strategy that is applicable is the best one
                break
        except Exception as e:
            pass

    candidates.sort(key=lambda s: s.get_compatibilities(), reverse=True)
    return candidates[0].get_type() if candidates else col.dtypes


def get_suggested_threshold(col: pd.Series) -> float:
    c = len(col)
    if c < 100:
        return 0.6
    elif c < 1000:
        return 0.7
    return 0.8