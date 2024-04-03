import os


# MinIO Config
BUCKET_NAME = os.getenv('APP_BUCKET_NAME', 'default')
MINIO_SERVER_HOST = os.getenv('APP_MINIO_SERVER_HOST', 'localhost')
MINIO_SERVER_ACCESS_KEY = os.getenv('APP_MINIO_SERVER_ACCESS_KEY', 'minio')
MINIO_SERVER_ACCESS_SECRET_KEY = os.getenv('APP_MINIO_SERVER_ACCESS_SECRET_KEY', 'miniosecret')
UPLOAD_EXPIRES = 300

# Storage Config
STORAGE_ADAPTERS = {
    'MinioStorageAdapter': {
        'kwargs': {
            'endpoint': MINIO_SERVER_HOST + ':9000',
            'access_key': MINIO_SERVER_ACCESS_KEY,
            'secret_key': MINIO_SERVER_ACCESS_SECRET_KEY,
            'bucket_name': BUCKET_NAME,
            'expires_in_seconds': UPLOAD_EXPIRES
        }
    }
}

PREFERRED_STORAGE_ADAPTER = 'MinioStorageAdapter'

# Broker Config
BROKER_HOST = os.getenv('APP_BROKER_HOST', 'localhost')
BROKER_PORT = os.getenv('APP_BROKER_PORT', '5672')
BROKER_USER = os.getenv('APP_BROKER_USER', 'guest')
BROKER_PASSWORD = os.getenv('APP_BROKER_PASSWORD', 'guest')
