import gc

import numpy as np
import pandas as pd
from celery.utils.log import get_task_logger

from type_inference.strategies import ALL_STRATEGIES, DatetimeConvertStrategy

logger = get_task_logger(__name__)


def infer_type_of_col(col: pd.Series, threshold=0.8) -> np.dtype:
    threshold = get_suggested_threshold(col) if threshold == "auto" else threshold
    strategies = map(lambda x: x(data=col, threshold=threshold), ALL_STRATEGIES)
    candidates = []
    for strategy in strategies:
        strategy_name = strategy.__class__.__name__
        if strategy_name == DatetimeConvertStrategy.__name__:  # Skip DateConvertStrategy
            continue
        try_strategy(strategy, threshold, candidates)
        if candidates and candidates[-1].get_compatibilities() == 1.0:
            break

    # Try datetime strategy if no other strategy is applicable
    if not candidates:
        logger.debug("No applicable strategy found. Trying DatetimeConvertStrategy")
        datetime_threshold = 0.1
        strategy = DatetimeConvertStrategy(data=col, threshold=datetime_threshold)
        try_strategy(strategy, datetime_threshold, candidates)

    candidates.sort(key=lambda s: s.get_compatibilities(), reverse=True)

    if candidates:
        logger.debug(f"Found {len(candidates)} candidates. Selected {candidates[0].__class__.__name__}")
    else:
        logger.debug("No candidates found")
    return candidates[0].get_type() if candidates else col.dtypes


def try_strategy(strategy, threshold, result_queue, ignore_threshold=False):
    logger.debug(f"Trying strategy {strategy.__class__.__name__} for column {strategy.data.name}")
    try:
        if not strategy.is_applicable():
            logger.debug(f"Strategy {strategy.__class__.__name__} not applicable")
            return
        if ignore_threshold or strategy.get_compatibilities() >= threshold:
            result_queue.append(strategy)
            logger.debug(
                f"Strategy {strategy.__class__.__name__} with compatibility {strategy.get_compatibilities()} is applicable")
        else:
            logger.debug(
                f"Strategy {strategy.__class__.__name__} not applicable (compatibility: {strategy.get_compatibilities()})")
        gc.collect()
    except Exception as e:
        logger.error(f"Error while applying strategy {strategy.__class__.__name__}: {e}")


def get_suggested_threshold(col: pd.Series) -> float:
    c = len(col)
    if c < 100:
        return 0.6
    elif c < 1000:
        return 0.7
    return 0.8
