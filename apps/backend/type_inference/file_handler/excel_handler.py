from collections import defaultdict

import pandas as pd

from storage import StorageService as storage_service
from .base import BaseFileHandler
from ..infer import infer_type_of_col


class ExcelHandler(BaseFileHandler):
    FIVE_MB = 5 * 1024 * 1024

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.columns_dtypes = defaultdict(set)

    def handle(self, *args, **kwargs):
        file_io = storage_service.download_file(filename=self.source)
        self._read_entire_file(file_io)

    def _read_entire_file(self, file_io):
        df = pd.read_excel(file_io)

        for col in df.columns:
            t = infer_type_of_col(df[col], threshold='auto')
            self.columns_dtypes[col].add(t)
