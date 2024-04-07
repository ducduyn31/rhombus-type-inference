from rest_framework.response import Response
from rest_framework.views import APIView

from infer_sessions.models import InferSession
from inferstate import InferStates


class MinIOWebhook(APIView):
    def post(self, request):
        webhook_data = request.data
        filename = webhook_data['Key']

        if filename:
            session_id = filename.split('/')[-1]
            model = InferSession.objects.filter(pk=session_id).first()
            if not model:
                return Response(status=200)
            process = model.to_infer_session_process()

            try:
                filename_without_bucket = "".join(filename.split('/')[1:])
                result = {
                    "filename": filename_without_bucket,
                }
                process.trigger(InferStates.FILE_UPLOADED, result=result)
            finally:
                return Response(status=200)

        return Response(status=200)