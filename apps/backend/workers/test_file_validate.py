from unittest.mock import patch

import requests
from rest_framework.test import APITestCase, APIClient

from config import MINIO_SERVER_HOST
from .file_validate import validate_file
from inferstate import InferStates


class FileValidationTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.storage_host = f"http://{MINIO_SERVER_HOST}:9000"

    def upload_file_from_assets(self, file_name):
        # Create a session
        response = self.client.post('/api/sessions/')
        session_id = response.data["data"]["session_id"]
        self.assertEqual(response.status_code, 201)
        # Generate upload link
        response = self.client.put(f'/api/sessions/{session_id}/', data={
            "state": "generate_presigned_url"
        })
        self.assertEqual(response.status_code, 200)
        upload_link = response.data["data"]["upload_url"]
        upload_link = self.storage_host + upload_link

        # Upload file
        with open(f'assets/{file_name}', 'rb') as file:
            response = requests.put(upload_link, data=file)

        self.assertEqual(response.status_code, 200)

        response = self.client.put(f'/api/sessions/{session_id}/', data={
            "state": "file_uploaded"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("filename", response.data["data"])

        return response.data["data"]

    @patch('workers.file_validate.validate_file.delay', side_effect=validate_file)
    @patch('workers.infer_data_types.infer_data_types')
    def test_file_validation_should_return_true_for_valid_file_with_eager_load(self, _1, _2):
        data = self.upload_file_from_assets('sample_data.csv')
        session_id = data["session_id"]
        response = self.client.get(f'/api/sessions/{session_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(InferStates.INFER_FILE, response.data["data"]["state"])

    @patch('workers.file_validate.validate_file.delay', side_effect=validate_file)
    @patch('workers.infer_data_types.infer_data_types')
    def test_file_validation_should_return_false_for_invalid_file_with_eager_load(self, _1, _2):
        data = self.upload_file_from_assets('not_a_valid_file.csv')
        session_id = data["session_id"]

        response = self.client.get(f'/api/sessions/{session_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(InferStates.ERROR, response.data["data"]["state"])
