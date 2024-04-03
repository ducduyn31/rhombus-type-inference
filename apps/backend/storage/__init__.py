from config import STORAGE_ADAPTERS, PREFERRED_STORAGE_ADAPTER
from .aws_adapter import AwsStorageAdapter

from .storage import StorageService as _StorageService
from .minio_adapter import MinioStorageAdapter

_adapters = [
    MinioStorageAdapter,
    AwsStorageAdapter,
]


def get_storage_adapter():
    adapter = STORAGE_ADAPTERS[PREFERRED_STORAGE_ADAPTER]
    for a in _adapters:
        if a.__name__ == PREFERRED_STORAGE_ADAPTER:
            return a(**adapter['kwargs'])
    return MinioStorageAdapter(**adapter['kwargs'])


StorageService = _StorageService(adapter=get_storage_adapter())
