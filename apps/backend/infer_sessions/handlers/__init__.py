from .init_state_handler import InitStateHandler
from .generate_url_state_handler import GenerateUrlStateHandler

def build_handler_map(handlers):
    handler_map = {}
    for handler in handlers:
        handler_map[handler.state] = handler
    return handler_map
