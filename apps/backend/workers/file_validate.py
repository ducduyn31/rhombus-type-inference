from pandas.errors import ParserError

from infer_sessions.models import InferSession
from storage import StorageService as storage_service
from .worker_app import app

ALLOWED_MIME_TYPES = [
    'text/csv',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
]

def try_reading_some_data_in_csv(filename):
    try:
        import pandas as pd
        file_io = storage_service.download_file(filename)
        iterator = pd.read_csv(file_io, iterator=True, chunksize=5)

        for chunk in iterator:
            if chunk.dtypes is not None:
                return True
            break

    except ParserError:
        return False


@app.task
def validate_file(session_id):
    session = InferSession.objects.filter(pk=session_id).first()
    is_valid, mime_type = is_valid_mime(session.file)
    process = session.to_infer_session_process()
    result = session.result

    if is_valid:
        result.update({
            "mime_type": mime_type,
        })
        process.trigger("next", result=result)
    elif mime_type == "text/plain" and try_reading_some_data_in_csv(session.file):
        result.update({
            "mime_type": "text/csv",
        })
        process.trigger("next", result=result)
    else:
        process.trigger("error")

    return is_valid

def is_valid_mime(filename):
    mime_type = storage_service.get_mimetype(filename=filename)

    return mime_type in ALLOWED_MIME_TYPES, mime_type