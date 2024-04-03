import magic

from storage import StorageService as storage_service
from .worker_app import app
from infer_sessions.models import InferSession

ALLOWED_MIME_TYPES = [
    'text/csv',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
]


@app.task
def validate_file(session_id):
    session = InferSession.objects.filter(pk=session_id).first()
    is_valid, mime_type = is_valid_mime(session.file)
    process = session.to_infer_session_process()

    if is_valid:
        result = {
            "mime_type": mime_type,
        }
        process.trigger("next", result=result)
    else:
        process.trigger("error")

    return is_valid

def is_valid_mime(filename):
    mime_type = storage_service.get_mimetype(filename=filename)

    return mime_type in ALLOWED_MIME_TYPES, mime_type