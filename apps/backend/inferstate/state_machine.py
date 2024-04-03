import enum

from transitions import Machine
from .callbacks_manager import callback_manager


class States(enum.Enum):
    INIT = 'init'
    GENERATE_PRESIGNED_URL = 'generate_presigned_url'
    FILE_UPLOADED = 'file_uploaded'
    VALIDATE_FILE = 'validate_file'
    INFER_FILE = 'infer_file'
    SUCCESS = 'success'
    ERROR = 'error'

    @staticmethod
    def get_choices():
        return [(state.value, state.name) for state in States]

    @staticmethod
    def all_states():
        return [state.value for state in States]

    @staticmethod
    def from_str(state_str):
        for state in States:
            if state.value == state_str:
                return state
        return None

    def __str__(self):
        return self.value

    def __eq__(self, other):
        return self.value == other

    def __hash__(self):
        return hash(self.value)


class InferSessionProcess(object):
    states = States

    def __init__(self, session_id, state=None, should_publish=True):
        self.should_publish_state_change = should_publish
        self.machine = Machine(model=self, states=self.states, initial=States.INIT)
        self._prepare_transitions()

        self.session_id = session_id
        if state and state in States.all_states():
            if type(state) == str:
                state = States.from_str(state)
            self.machine.set_state(state)

    def _state_change_publish(self, *args, **kwargs):
        if not self.should_publish_state_change:
            return
        current_state = self.state
        callback_manager.execute_callbacks(current_state, self, *args, **kwargs)

    def _prepare_transitions(self):
        self.machine.add_transition(States.GENERATE_PRESIGNED_URL.value, States.INIT, States.GENERATE_PRESIGNED_URL,
                                    after='_state_change_publish')
        self.machine.add_transition(States.FILE_UPLOADED.value, States.GENERATE_PRESIGNED_URL, States.FILE_UPLOADED,
                                    after='_state_change_publish')
        self.machine.add_transition(States.VALIDATE_FILE.value, States.FILE_UPLOADED, States.VALIDATE_FILE,
                                    after='_state_change_publish')
        self.machine.add_transition(States.INFER_FILE.value, States.VALIDATE_FILE, States.INFER_FILE,
                                    after='_state_change_publish')
        self.machine.add_transition(States.SUCCESS.value, States.INFER_FILE, States.SUCCESS,
                                    after='_state_change_publish')
        self.machine.add_transition(States.ERROR.value, '*', States.ERROR, after='_state_change_publish')

        self.machine.add_transition('next', States.INIT, States.GENERATE_PRESIGNED_URL, after='_state_change_publish')
        self.machine.add_transition('next', States.GENERATE_PRESIGNED_URL, States.FILE_UPLOADED,
                                    after='_state_change_publish')
        self.machine.add_transition('next', States.FILE_UPLOADED, States.VALIDATE_FILE, after='_state_change_publish')
        self.machine.add_transition('next', States.VALIDATE_FILE, States.INFER_FILE, after='_state_change_publish')
        self.machine.add_transition('next', States.INFER_FILE, States.SUCCESS, after='_state_change_publish')
