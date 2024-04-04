import requests
from rest_framework.test import APITestCase, APIClient
from config import MINIO_SERVER_HOST


class FileInferTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.storage_host = f"http://{MINIO_SERVER_HOST}:9000"


    def upload_file_from_assets(self, file_name):
        # Create a session
        response = self.client.post('/api/sessions/' )
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

    def test_infer_types_should_return_type_of_file(self):
        data = self.upload_file_from_assets('sample_data.csv')
        session_id = data["session_id"]
        response = self.client.get(f'/api/sessions/{session_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["data"]["state"], "infer_file")