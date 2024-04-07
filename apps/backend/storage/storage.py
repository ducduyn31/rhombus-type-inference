from io import BytesIO


class AbstractStorageAdapter:
    def generate_upload_url(self, filename: str, get_full_url = False) -> str:
        raise NotImplementedError

    def generate_get_url(self, filename: str, get_full_url = False) -> str:
        raise NotImplementedError

    def download_file(self, filename: str) -> BytesIO:
        raise NotImplementedError

    def download_partial_file(self, filename: str, start: int, end: int) -> BytesIO:
        raise NotImplementedError

    def upload_file(self, filename: str, file):
        raise NotImplementedError

    def get_mimetype(self, filename: str) -> str:
        raise NotImplementedError

    def get_file_size(self, filename: str) -> int:
        raise NotImplementedError

class StorageService:
    def __init__(self, adapter: AbstractStorageAdapter):
        self.adapter = adapter

    def generate_upload_url(self, filename: str, get_full_url= False) -> str:
        return self.adapter.generate_upload_url(filename, get_full_url=get_full_url)

    def generate_get_url(self, filename: str, get_full_url = False) -> str:
        return self.adapter.generate_get_url(filename, get_full_url=get_full_url)

    def download_file(self, filename: str) -> BytesIO:
        return self.adapter.download_file(filename)

    def download_partial_file(self, filename: str, start: int, end: int) -> BytesIO:
        return self.adapter.download_partial_file(filename, start, end)

    def upload_file(self, filename: str, file):
        self.adapter.upload_file(filename, file)

    def get_mimetype(self, filename: str) -> str:
        return self.adapter.get_mimetype(filename)

    def get_file_size(self, filename: str) -> int:
        return self.adapter.get_file_size(filename)