from collections import defaultdict

import pandas as pd

from storage import StorageService as storage_service
from workers.persist_infer_results import persist_results
from .base import BaseFileHandler
from ..infer import infer_type_of_col


class ExcelFileHandler(BaseFileHandler):
    FIVE_MB = 5 * 1024 * 1024

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def handle(self, *args, **kwargs):
        file_io = storage_service.download_file(filename=self.source)
        self._read_entire_file(file_io)

    def _read_entire_file(self, file_io):
        df = pd.read_excel(file_io)
        result = defaultdict(set)
        for col in df.columns:
            t = infer_type_of_col(df[col], threshold='auto')
            result[col].add(str(t))

        # Convert set to list
        result = {k: list(v) for k, v in result.items()}
        persist_results.delay(result, self.entity_id)
