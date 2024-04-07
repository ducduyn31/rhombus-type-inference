from unittest.mock import patch

import ulid
from rest_framework.test import APIClient, APITestCase

from inferstate import InferStates


# Create your tests here.
class InferSessionAPITestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

    @staticmethod
    def is_ulid(ulid_str):
        try:
            ulid.parse(ulid_str)
            return True
        except ValueError:
            return False

    def test_infer_session_should_start_new_session(self):
        response = self.client.post("/sessions/")
        self.assertEqual(response.status_code, 201)
        session_id = response.data["data"]["session_id"]
        state = response.data["data"]["state"]

        self.assertTrue(self.is_ulid(session_id))
        self.assertEqual(str(InferStates.INIT), state)

    def test_infer_session_should_fetch_by_id(self):
        response = self.client.post("/sessions/")
        session_id = response.data["data"]["session_id"]

        response = self.client.get(f"/sessions/{session_id}/")
        session_id_2 = response.data["data"]["session_id"]
        self.assertEqual(session_id, session_id_2)

    def test_infer_session_should_fail_if_id_not_exists(self):
        response = self.client.get("/sessions/notfound/")
        self.assertEqual(400, response.status_code)

        valid_ulid = ulid.new().str
        response = self.client.get(f"/sessions/{valid_ulid}/")
        self.assertEqual(404, response.status_code)

    def test_infer_session_should_get_presigned_url(self):
        response = self.client.post("/sessions/")
        session_id = response.data["data"]["session_id"]

        response = self.client.put(f"/sessions/{session_id}/", data={
            "state": "generate_presigned_url",
            "filename": "test.csv"
        })
        self.assertEqual(200, response.status_code)
        self.assertIn("upload_url", response.data["data"])
        self.assertEqual(InferStates.GENERATE_PRESIGNED_URL, response.data["data"]["state"])

    def test_infer_session_should_not_move_to_next_state_if_file_is_not_uploaded(self):
        response = self.client.post("/sessions/")
        session_id = response.data["data"]["session_id"]

        response = self.client.put(f"/sessions/{session_id}/", data={
            "state": "generate_presigned_url",
            "filename": "test.csv"
        })
        self.assertEqual(200, response.status_code)
        self.assertEqual(InferStates.GENERATE_PRESIGNED_URL, response.data["data"]["state"])

        response = self.client.put(f"/sessions/{session_id}/", data={
            "state": "generate_presigned_url"
        })
        self.assertEqual(200, response.status_code)
        self.assertEqual(InferStates.GENERATE_PRESIGNED_URL, response.data["data"]["state"])

    def test_infer_session_should_fail_if_state_is_invalid(self):
        response = self.client.post("/sessions/")
        session_id = response.data["data"]["session_id"]

        response = self.client.put(f"/sessions/{session_id}/", data={
            "state": "invalid_state"
        })
        self.assertEqual(400, response.status_code)

    def test_infer_session_should_fail_if_state_is_invalid_for_current_state(self):
        response = self.client.post("/sessions/")
        session_id = response.data["data"]["session_id"]

        response = self.client.put(f"/sessions/{session_id}/", data={
            "state": "generate_presigned_url",
            "filename": "test.csv"
        })
        self.assertEqual(200, response.status_code)
        self.assertEqual(InferStates.GENERATE_PRESIGNED_URL, response.data["data"]["state"])

        response = self.client.put(f"/sessions/{session_id}/", data={
            "state": "validate_file"
        })
        self.assertEqual(400, response.status_code)

    @patch("workers.file_validate.validate_file.delay")
    def test_infer_session_should_move_to_validate_file_state_automatically(self, mocked_validate_file):
        mocked_validate_file.return_value = None

        response = self.client.post("/sessions/")
        session_id = response.data["data"]["session_id"]

        response = self.client.put(f"/sessions/{session_id}/", data={
            "state": "generate_presigned_url",
            "filename": "test.csv"
        })
        self.assertEqual(200, response.status_code)

        response = self.client.put(f"/sessions/{session_id}/", data={
            "state": "file_uploaded"
        })
        self.assertEqual(InferStates.VALIDATE_FILE, response.data["data"]["state"])
