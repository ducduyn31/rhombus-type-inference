import ulid
from rest_framework import viewsets, status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from inferstate import InferStates
from storage import StorageService
from .handlers import build_handler_map, InitStateHandler, GenerateUrlStateHandler
from .models import InferSession
from .serializers import InferSessionSerializer, InferSessionUpdateSerializer


# Create your views here.
class InferSessionViewSet(viewsets.ModelViewSet):
    queryset = InferSession.objects.all()
    serializer_class = InferSessionSerializer
    storage_service = StorageService
    handlers = build_handler_map(handlers=[
        InitStateHandler(serializer=serializer_class),
        GenerateUrlStateHandler(serializer=serializer_class),
    ])

    def create(self, request, **kwargs):
        session = InferSession.objects.create(
            state=InferStates.INIT,
        )
        return self._build_response(status_code=status.HTTP_201_CREATED, session=session)

    def retrieve(self, request, pk=None, **kwargs):
        session, error_message = self._get_session(pk)

        if error_message:
            return error_message

        return self._build_response(status_code=status.HTTP_200_OK, session=session)

    def update(self, request, pk=None, **kwargs):
        session, error_message = self._get_session(pk)

        if error_message:
            return error_message

        content = InferSessionUpdateSerializer(data=request.data, context={"session": session, "request": request})

        if not content.is_valid():
            return self._build_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message='Invalid request',
                description=content.errors
            )

        data = content.validated_data

        if session.state not in self.handlers:
            return self._build_response(
                status_code=status.HTTP_200_OK,
                message='Session is not updated',
            )

        handler = self.handlers[session.state]
        try:
            response = handler.handle(session, data)
        except APIException as e:
            return self._build_response(
                status_code=e.get_codes(),
                description=e.detail,
            )

        if not response:
            return self._build_response(
                status_code=status.HTTP_200_OK,
                session=session,
                message='Session is not updated',
            )

        return self._build_response(**response)

    def validate_next_state(self, session, next_state):
        if session.state not in self.handlers:
            return False

        handler = self.handlers[session.state]
        return handler.validate_next_state(next_state)

    def _build_response(self, status_code, session=None, data=None, message=None, description=None):
        response_data = dict()
        code = status_code

        response_error = dict(
            code=code,
            description=description,
        )

        if session:
            serializer = self.get_serializer(session)
            result = serializer.data["result"]
            session_error = serializer.data["error"]
            if result:
                response_data.update(result)
            if session_error:
                response_error.update(session_error)
                if session_error.get("code"):
                    code = session_error["code"]
                    message = session_error["message"]
            response_data.update(dict(session_id=f"{session.pk}", state=f"{session.state}"))

        if data:
            response_data.update(data)

        default_message = {
            status.HTTP_201_CREATED: 'Session created',
            status.HTTP_200_OK: 'Request successful',
            status.HTTP_400_BAD_REQUEST: 'Bad request',
        }

        if not message:
            message = default_message[code]

        response = dict(
            message=message,
            error=response_error if not status.is_success(code) else None,
            data=response_data,
        )

        return Response(response, status=status_code)

    def _get_session(self, key):
        try:
            ulid.parse(key)
        except ValueError:
            return None, self._build_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message='Invalid session ID',
                description='Session ID is not a valid ULID'
            )

        session = InferSession.objects.filter(pk=key).first()

        if not session:
            return None, self._build_response(
                status_code=status.HTTP_404_NOT_FOUND,
                message='Session not found',
                description='Session ID does not exist'
            )

        return session, None
