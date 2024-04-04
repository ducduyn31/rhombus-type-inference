from .base import BaseFileHandler
from storage import StorageService as storage_service

class CsvFileHandler(BaseFileHandler):

    def __init__(self):
        super().__init__()

    def handle(self, *args, **kwargs):
        file = storage_service.download_file(filename=self.source)




