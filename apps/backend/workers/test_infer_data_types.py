from unittest.mock import patch

import requests
from rest_framework.test import APITestCase, APIClient

from config import MINIO_SERVER_HOST
from inferstate import InferStates
from type_inference.tasks import infer_data_types_of_chunk
from workers.file_validate import validate_file
from workers.infer_data_types import infer_data_types


class FileInferTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.storage_host = f"http://{MINIO_SERVER_HOST}:9000"

    def upload_file_from_assets(self, file_name):
        # Create a session
        response = self.client.post('/sessions/')
        session_id = response.data["data"]["session_id"]
        self.assertEqual(response.status_code, 201)
        # Generate upload link
        response = self.client.put(f'/sessions/{session_id}/', data={
            "state": "generate_presigned_url"
        })
        self.assertEqual(response.status_code, 200)
        upload_link = response.data["data"]["upload_url"]
        upload_link = self.storage_host + upload_link

        # Upload file
        with open(f'assets/{file_name}', 'rb') as file:
            response = requests.put(upload_link, data=file)

        self.assertEqual(response.status_code, 200)

        response = self.client.put(f'/sessions/{session_id}/', data={
            "state": "file_uploaded"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("filename", response.data["data"])

        return response.data["data"]

    def infer_type_from_header(self, name):
        names_to_types = {
            "id": "integer",
            "name": "string",
            "non_standard_date": "date",
            "email": "string",
            "mixed_names_with_nulls": "string",
            "mixed_dates_with_nulls": "date",
            "very_large_number": "integer",
            "category": "category",
        }

    @patch('workers.file_validate.validate_file.delay', side_effect=validate_file)
    @patch('workers.infer_data_types.infer_data_types.delay', side_effect=infer_data_types)
    def test_infer_types_should_return_type_of_file(self, _1, mocked_infer_data_types):
        data = self.upload_file_from_assets('sample_data.csv')
        session_id = data["session_id"]
        mocked_infer_data_types.assert_called_with(session_id)
        response = self.client.get(f'/sessions/{session_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(InferStates.SUCCESS, response.data["data"]["state"])

        expected_types = {
            "Name": "object",
            "Grade": "category",
            "Birthdate": "datetime64[ns]",
            "Score": "float32",
        }

        self.assertDictEqual(expected_types, response.data["data"]["columns_dtypes"])

    @patch('workers.file_validate.validate_file.delay', side_effect=validate_file)
    @patch('workers.infer_data_types.infer_data_types.delay', side_effect=infer_data_types)
    @patch('type_inference.tasks.infer_data_types_of_chunk.delay', side_effect=infer_data_types_of_chunk)
    def test_infer_types_of_large_file_should_return_type_of_file(self, _1, _2, _3):
        data = self.upload_file_from_assets('large_file.csv')
        session_id = data["session_id"]
        response = self.client.get(f'/sessions/{session_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(InferStates.SUCCESS, response.data["data"]["state"])

        expected_types = {
            "Transaction ID": "object",
            "Customer ID": "object",
            "Transaction Amount": "float32",
            "Transaction Date": "datetime64[ns]",
            "Payment Method": "category",
            "Product Category": "category",
            "Quantity": "uint8",
            "Customer Age": "int8",
            "Customer Location": "object",
            "Device Used": "category",
            "IP Address": "object",
            "Shipping Address": "object",
            "Billing Address": "object",
            "Is Fraudulent": "bool",
            "Account Age Days": "uint16",
            "Transaction Hour": "uint8",
        }

        self.assertDictEqual(expected_types, response.data["data"]["columns_dtypes"])

    @patch('workers.file_validate.validate_file.delay', side_effect=validate_file)
    @patch('workers.infer_data_types.infer_data_types.delay', side_effect=infer_data_types)
    def test_infer_types_of_test_1_should_return_type_of_file(self, _1, mocked_infer_data_types):
        data = self.upload_file_from_assets('test_1.csv')
        session_id = data["session_id"]
        mocked_infer_data_types.assert_called_with(session_id)
        response = self.client.get(f'/sessions/{session_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(InferStates.SUCCESS, response.data["data"]["state"])

    @patch('workers.file_validate.validate_file.delay', side_effect=validate_file)
    @patch('workers.infer_data_types.infer_data_types.delay', side_effect=infer_data_types)
    def test_infer_types_of_test_2_should_return_type_of_file(self, _1, mocked_infer_data_types):
        data = self.upload_file_from_assets('test_2.csv')
        session_id = data["session_id"]
        mocked_infer_data_types.assert_called_with(session_id)
        response = self.client.get(f'/sessions/{session_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(InferStates.SUCCESS, response.data["data"]["state"])

    @patch('workers.file_validate.validate_file.delay', side_effect=validate_file)
    @patch('workers.infer_data_types.infer_data_types.delay', side_effect=infer_data_types)
    def test_infer_types_of_test_13_should_return_type_of_file(self, _1, mocked_infer_data_types):
        data = self.upload_file_from_assets('test_13.csv')
        session_id = data["session_id"]
        mocked_infer_data_types.assert_called_with(session_id)
        response = self.client.get(f'/sessions/{session_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(InferStates.SUCCESS, response.data["data"]["state"])
