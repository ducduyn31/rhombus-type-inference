from collections import defaultdict

from .base import BaseFileHandler
from storage import StorageService as storage_service
import pandas as pd


class CsvFileHandler(BaseFileHandler):
    FIVE_MB = 5 * 1024 * 1024

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.columns_dtypes = defaultdict(set)

    def handle(self, *args, **kwargs):
        file_size = storage_service.get_file_size(filename=self.source)
        file_io = storage_service.download_file(filename=self.source)

        if file_size < self.FIVE_MB:
            self._read_entire_file(file_io)
        else:
            self._read_file_in_chunks(file_io)

    def _read_entire_file(self, file_io):
        df = pd.read_csv(file_io)

        for col in df.columns:
            self.columns_dtypes[col].add(df[col].dtype)

    def _read_file_in_chunks(self, file_io):
        iterator = pd.read_csv(file_io, iterator=True, chunksize=1000)
        for chunk in iterator:
            for col in chunk.columns:
                self.columns_dtypes[col].add(chunk[col].dtype)
