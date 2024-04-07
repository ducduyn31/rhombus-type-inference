from collections import defaultdict

from .base import BaseFileHandler
from storage import StorageService as storage_service
import pandas as pd
from ..infer import infer_type_of_col
from ..tasks import infer_data_types_of_chunk


class CsvFileHandler(BaseFileHandler):
    FIFTY_MB = 50 * 1024 * 1024
    CHUNK_SIZE = 300_000

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.columns_dtypes = defaultdict(set)

    def handle(self, *args, **kwargs):
        file_size = storage_service.get_file_size(filename=self.source)
        file_io = storage_service.download_file(filename=self.source)

        if file_size < self.FIFTY_MB:
            self._read_entire_file(file_io)
        else:
            self._read_file_in_chunks(file_io)

    def _read_entire_file(self, file_io):
        df = pd.read_csv(file_io)

        for col in df.columns:
            t = infer_type_of_col(df[col], threshold='auto')
            self.columns_dtypes[col].add(t)

    def _read_file_in_chunks(self, file_io):
        iterator = pd.read_csv(file_io, iterator=True, chunksize=self.CHUNK_SIZE)
        part_number = 0
        for _ in iterator:
            types = infer_data_types_of_chunk.delay(source=self.source, part_number=part_number, chunk_size=self.CHUNK_SIZE)
            for col in types:
                self.columns_dtypes[col].add(types[col])
            #TODO Break the loop for now, remove this line when the task is implemented
            part_number += 1
            break
