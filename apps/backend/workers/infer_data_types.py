from type_inference.file_handler import CsvFileHandler
from workers.worker_app import app

file_handlers = {
    "text/csv": CsvFileHandler,
}


@app.task
def infer_data_types(session_id, **kwargs):
    from infer_sessions.models import InferSession
    session = InferSession.objects.filter(pk=session_id).first()

    if not session:
        return

    mime_type = session.result.get("mime_type")

    result = session.result
    process = session.to_infer_session_process()

    for allowed_mime_type in file_handlers:
        if allowed_mime_type == mime_type:
            file_handler = file_handlers[allowed_mime_type](source=session.file)
            try:
                file_handler.handle()
            except Exception as e:
                err = {
                    "code": 400,
                    "message": type(e).__name__,
                    "description": str(e)
                }
                process.trigger("error", error=err)
                return

            result.update({
                "columns_dtypes": {
                    col_name: str(list(dtypes)[0]) for col_name, dtypes in file_handler.columns_dtypes.items()
                }
            })
            break

    process.trigger('next', result=result)
