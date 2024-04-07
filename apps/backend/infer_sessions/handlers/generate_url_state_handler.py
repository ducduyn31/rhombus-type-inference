from datetime import datetime

from rest_framework import status

from inferstate import InferStates
from storage import StorageService
from .handler import BaseHandler


class GenerateUrlStateHandler(BaseHandler):
    storage_service = StorageService

    def __init__(self, serializer):
        super().__init__(InferStates.GENERATE_PRESIGNED_URL, serializer=serializer)

    def handle(self, model, data):
        """
        Move from generate presigned url state to file uploaded state
        :param model: Django model
        :param data: Serialized request from users
        """

        # Regenerate the presigned URL
        if model.state == data["state"] == InferStates.GENERATE_PRESIGNED_URL:
            today = datetime.now().strftime("%Y-%m-%d")
            # origin_filename = data.get("filename", ".csv")
            # preferred_extension = origin_filename.split(".")[-1]
            # filename = f"{today}/{model.pk}.{preferred_extension}"
            filename = f"{today}/{model.pk}"
            updated_url = self.storage_service.generate_upload_url(filename=filename)
            result = {
                "upload_url": updated_url,
            }
            model.file = filename
            model.result = result
            model.save()

            return self.build_response(
                status_code=status.HTTP_200_OK,
                model=model,
                extra_data=dict(upload_url=updated_url),
            )

        # Move to file uploaded state
        process = model.to_infer_session_process()
        result = {
            "filename": model.file,
        }
        process.trigger(data["state"], result=result)

        model.refresh_from_db()

        return self.build_response(
            status_code=status.HTTP_200_OK,
            model=model,
        )