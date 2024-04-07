import uuid
from datetime import datetime

from rest_framework import status

from inferstate import InferStates
from storage import StorageService
from .handler import BaseHandler


class InitStateHandler(BaseHandler):
    storage_service = StorageService

    def __init__(self, serializer):
        super().__init__(InferStates.INIT, serializer)

    def handle(self, model, data):
        """
        Move from init state to generate presigned url state
        :param model: Django model
        :param data: Serialized request from users
        """
        today = datetime.now().strftime("%Y-%m-%d")
        # origin_filename = data.get("filename", ".csv")
        # preferred_extension = origin_filename.split(".")[-1]
        filename = f"{today}/{model.session_id}"
        presigned_url = self.storage_service.generate_upload_url(filename=filename)
        process = model.to_infer_session_process()
        result = {
            "upload_url": presigned_url,
        }

        # Move to generate presigned url state and update the model
        process.trigger(data["state"], result=result, file=filename)

        model.refresh_from_db()

        return self.build_response(
            status_code=status.HTTP_200_OK,
            model=model,
            extra_data=dict(upload_url=presigned_url),
        )
