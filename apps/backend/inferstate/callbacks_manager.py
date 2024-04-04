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


def callback(states=None, without=None):
    """a decorator to register a callback for a state"""

    def decorator(fn):
        from .state_machine import States
        register_states = set(States) if states is None else set(states)
        if without:
            register_states = register_states - set(without)

        for state in register_states:
            callback_manager.register(state, fn)

        return fn

    return decorator
