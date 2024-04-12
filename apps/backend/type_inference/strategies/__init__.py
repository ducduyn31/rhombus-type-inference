from .boolean import BooleanConvertStrategy
from .categorical import CategoricalConvertStrategy
from .datetime import DatetimeConvertStrategy
from .numeric import NumericConvertStrategy

ALL_STRATEGIES = [
    BooleanConvertStrategy,
    NumericConvertStrategy,
    CategoricalConvertStrategy,
    # DatetimeConvertStrategy,
]
