from datetime import timedelta
from io import BytesIO
from urllib.parse import urlparse

from minio import Minio
import magic

from storage.storage import AbstractStorageAdapter


class MinioStorageAdapter(AbstractStorageAdapter):
    def __init__(self, endpoint: str, access_key: str, secret_key: str, bucket_name: str, expires_in_seconds: int):
        self.minio_client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=False
        )
        self.bucket_name = bucket_name
        self.expires_in_seconds = expires_in_seconds

    def generate_upload_url(self, filename: str, get_full_url= False) -> str:
        full_url = self.minio_client.presigned_put_object(
            bucket_name=self.bucket_name,
            object_name=filename,
            expires=timedelta(seconds=self.expires_in_seconds)
        )

        if get_full_url:
            return full_url

        parsed_url = urlparse(full_url)
        return f"{parsed_url.path}?{parsed_url.query}"

    def generate_get_url(self, filename: str, get_full_url= False) -> str:
        full_url = self.minio_client.presigned_get_object(
            bucket_name=self.bucket_name,
            object_name=filename,
            expires=timedelta(seconds=self.expires_in_seconds)
        )

        if get_full_url:
            return full_url

        parsed_url = urlparse(full_url)
        return f"{parsed_url.path}?{parsed_url.query}"

    def download_file(self, filename: str) -> BytesIO:
        response = None
        try:
            response = self.minio_client.get_object(
                bucket_name=self.bucket_name,
                object_name=filename
            )
            return BytesIO(response.read())
        finally:
            response.close()
            response.release_conn()

    def download_partial_file(self, filename: str, start: int, end: int) -> BytesIO:
        response = None
        try:
            response = self.minio_client.get_object(
                bucket_name=self.bucket_name,
                object_name=filename,
                offset=start,
                length=end - start
            )
            return BytesIO(response.read())
        finally:
            response.close()
            response.release_conn()


    def upload_file(self, filename: str, file):
        self.minio_client.put_object(
            bucket_name=self.bucket_name,
            object_name=filename,
            data=file,
            length=-1,
            part_size=10 * 1024 * 1024,
        )

    def get_mimetype(self, filename: str) -> str:
        response = None
        try:
            response = self.minio_client.get_object(
                bucket_name=self.bucket_name,
                object_name=filename,
                length=100
            )
            filebuffer = response.read()
        finally:
            response.close()
            response.release_conn()

        m = magic.Magic(mime=True)
        mimetype = m.from_buffer(filebuffer)
        return mimetype

    def get_file_size(self, filename: str) -> int:
        response = self.minio_client.stat_object(
            bucket_name=self.bucket_name,
            object_name=filename
        )
        return response.size

    def list_file(self):
        objects = self.minio_client.list_objects(
            bucket_name=self.bucket_name
        )
        return [obj.object_name for obj in objects]

    def delete_file(self, filename: str):
        self.minio_client.remove_object(
            bucket_name=self.bucket_name,
            object_name=filename
       )
