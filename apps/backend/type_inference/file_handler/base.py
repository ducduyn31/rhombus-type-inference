class BaseFileHandler:
    
    def __init__(self, source, session_id):
        self.source = source
        self.entity_id = session_id

    def handle(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented")
