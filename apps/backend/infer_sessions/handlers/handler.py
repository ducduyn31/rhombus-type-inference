from inferstate import InferStates


class BaseHandler:
    def __init__(self, state: InferStates, serializer):
        self.state = state
        self.serializer = serializer

    def handle(self, model, data):
        raise NotImplementedError

    def build_response(self,
                       status_code,
                       model=None,
                       extra_data=None,
                       message=None,
                       description=None
                       ):
        data =dict()

        if extra_data:
            data.update(extra_data)

        response = dict(
            status_code=status_code,
            data=data,
            message=message,
            description=description
        )

        if model:
            response.update(session=model)

        return response
