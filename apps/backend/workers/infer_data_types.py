import pandas as pd

from workers.worker_app import app
from type_inference.file_handler import CsvFileHandler


def infer_and_convert_data_types(df):
    for col in df.columns:
        # Attempt to convert to numeric first
        df_converted = pd.to_numeric(df[col], errors='coerce')
        if not df_converted.isna().all():  # If at least one value is numeric
            df[col] = df_converted
            continue

        # Attempt to convert to datetime
        try:
            df[col] = pd.to_datetime(df[col])
            continue
        except (ValueError, TypeError):
            pass

        # Check if the column should be categorical
        if len(df[col].unique()) / len(df[col]) < 0.5:  # Example threshold for categorization
            df[col] = pd.Categorical(df[col])

    return df

file_handlers = {
    "text/csv": CsvFileHandler,
}

@app.task
def infer_data_types(session_id, row_count=1000, offset=0, **kwargs):
    from infer_sessions.models import InferSession
    session = InferSession.objects.filter(pk=session_id).first()

    if not session:
        return

    mime_type = session.result.get("mime_type")

    for allowed_mime_type in file_handlers:
        if allowed_mime_type == mime_type:
            file_handler = file_handlers[allowed_mime_type](source=session.file)
            file_handler.handle()
            break

