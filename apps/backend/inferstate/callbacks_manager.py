from collections import defaultdict

class StateChangeCallbackManager:
    def __init__(self):
        self.callbacks = defaultdict(list)

    def register(self, state, callback):
        self.callbacks[state].append(callback)

    def get_callbacks(self, state):
        return self.callbacks.get(state, [])

    def execute_callbacks(self, state, session_machine, *args, **kwargs):
        callbacks = self.get_callbacks(state)
        for callback in callbacks:
            callback(session_machine, *args, **kwargs)


callback_manager = StateChangeCallbackManager()

def register_for_states(states, callbacks):
    for state in states:
        for callback in callbacks:
            callback_manager.register(state, callback)
