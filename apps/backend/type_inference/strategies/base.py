import numpy as np


class BaseConvertStrategy:

    def __init__(self, data, threshold=0.8):
        self.data = data
        self.threshold = threshold

    def is_applicable(self) -> bool:
        return True

    def get_type(self) -> np.dtype:
        raise NotImplementedError

    def get_compatibilities(self) -> float:
        return 0

    def convert(self):
        raise NotImplementedError
