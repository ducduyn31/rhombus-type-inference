from io import BytesIO
from urllib.parse import urlparse

import boto3
import magic

from storage.storage import AbstractStorageAdapter


class AwsStorageAdapter(AbstractStorageAdapter):
    def __init__(self, endpoint, access_key, secret_key, bucket_name, expires_in_seconds):
        self.client = boto3.client(
            's3',
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            config=boto3.session.Config(signature_version='s3v4')
        )
        self.bucket_name = bucket_name
        self.expires_in_seconds = expires_in_seconds

    def generate_upload_url(self, filename: str, get_full_url= False) -> str:
        full_url = self.client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': self.bucket_name,
                'Key': filename,
            },
            ExpiresIn=self.expires_in_seconds
        )

        if get_full_url:
            return full_url

        parsed_url = urlparse(full_url)
        return f"{parsed_url.path}?{parsed_url.query}"

    def generate_get_url(self, filename: str, get_full_url = False) -> str:
        full_url = self.client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': self.bucket_name,
                'Key': filename,
            },
            ExpiresIn=self.expires_in_seconds
        )

        if get_full_url:
            return full_url

        parsed_url = urlparse(full_url)
        return f"{parsed_url.path}?{parsed_url.query}"

    def download_file(self, filename: str) -> BytesIO:
        response = self.client.get_object(Bucket=self.bucket_name, Key=filename)
        return response['Body']


    def download_partial_file(self, filename: str, start: int, end: int) -> BytesIO:
        response = self.client.get_object(Bucket=self.bucket_name, Key=filename, Range=f"bytes={start}-{end}")
        return response['Body']

    def upload_file(self, filename: str, file):
        self.client.upload_fileobj(file, self.bucket_name, filename)

    def get_mimetype(self, filename: str) -> str:
        response = self.client.get_object(Bucket=self.bucket_name, Key=filename, Range='bytes=0-100')

        m = magic.Magic(mime=True)
        return m.from_buffer(response['Body'].read(100))

    def get_file_size(self, filename: str) -> int:
        response = self.client.head_object(Bucket=self.bucket_name, Key=filename)
        return response['ContentLength']

    def list_file(self):
        response = self.client.list_objects(Bucket=self.bucket_name)
        if 'Contents' not in response:
            return []
        contents = response['Contents']
        return [content['Key'] for content in contents]

    def delete_file(self, filename: str):
        self.client.delete_object(Bucket=self.bucket_name, Key=filename)
