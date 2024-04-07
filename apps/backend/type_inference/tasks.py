import pandas as pd

from type_inference.infer import infer_type_of_col
from workers.worker_app import app
from storage import StorageService as storage_service


@app.task
def infer_data_types_of_chunk(source, part_number, chunk_size, **kwargs):
    file_io = storage_service.download_file(filename=source)
    iterator = pd.read_csv(file_io, iterator=True, chunksize=chunk_size, skiprows=part_number * chunk_size)
    result = {}

    for chunk in iterator:
        for col in chunk.columns:
            t = infer_type_of_col(chunk[col], threshold='auto')
            result[col] = t
        break

    return result
