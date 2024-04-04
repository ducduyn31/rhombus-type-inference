from unittest.mock import patch

from django.test import TestCase, tag
import ulid

from infer_sessions.models import InferSession
from inferstate.state_machine import InferSessionProcess, States as InferStates


class InferStateTestCase(TestCase):

    def setUp(self):
        self.session_id = ulid.new().str
        self.machine = InferSessionProcess(session_id=self.session_id, should_publish=False)

    def test_state_machine_should_follow_the_expected_states(self):
        self.assertEqual(self.machine.state, InferStates.INIT)

        self.machine.generate_presigned_url()
        self.assertEqual(self.machine.state, InferStates.GENERATE_PRESIGNED_URL)

        self.machine.file_uploaded()
        self.assertEqual(self.machine.state, InferStates.FILE_UPLOADED)

        self.machine.validate_file()
        self.assertEqual(self.machine.state, InferStates.VALIDATE_FILE)

        self.machine.infer_file()
        self.assertEqual(self.machine.state, InferStates.INFER_FILE)

        self.machine.success()
        self.assertEqual(self.machine.state, InferStates.SUCCESS)

        self.machine.error()
        self.assertEqual(self.machine.state, InferStates.ERROR)

    def test_machine_next_should_automatically_move_to_next_state(self):
        self.assertEqual(self.machine.state, InferStates.INIT)
        self.machine.next()
        self.assertEqual(self.machine.state, InferStates.GENERATE_PRESIGNED_URL)
        self.machine.next()
        self.assertEqual(self.machine.state, InferStates.FILE_UPLOADED)
        self.machine.next()
        self.assertEqual(self.machine.state, InferStates.VALIDATE_FILE)
        self.machine.next()
        self.assertEqual(self.machine.state, InferStates.INFER_FILE)
        self.machine.next()
        self.assertEqual(self.machine.state, InferStates.SUCCESS)
        self.machine.error()
        self.assertEqual(self.machine.state, InferStates.ERROR)

    @tag('skip_setup')
    @patch("infer_sessions.models.InferSession.objects.get")
    @patch("inferstate.callbacks_manager.callback_manager.execute_callbacks")
    def test_machine_can_be_loaded_with_state(self, mocked_get, mocked_execute_callbacks):
        mocked_execute_callbacks.return_value = None
        mocked_get.return_value = InferSession()
        machine = InferSessionProcess(session_id=self.session_id, state=InferStates.FILE_UPLOADED)
        machine.next()
        self.assertEqual(machine.state, InferStates.VALIDATE_FILE)
