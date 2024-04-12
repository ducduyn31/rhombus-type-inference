from .boolean import BooleanConvertStrategy
from .categorical import CategoricalConvertStrategy
from .datetime import DatetimeConvertStrategy
from .numeric import NumericConvertStrategy
from .complex import ComplexNumberConvertStrategy
from .timedelta import TimedeltaConvertStrategy

ALL_STRATEGIES = [
    BooleanConvertStrategy,
    NumericConvertStrategy,
    CategoricalConvertStrategy,
    ComplexNumberConvertStrategy,
    TimedeltaConvertStrategy,
    # DatetimeConvertStrategy,
]
