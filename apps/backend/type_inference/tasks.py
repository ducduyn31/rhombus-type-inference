import gc

import pandas as pd
from celery.utils.log import get_task_logger

from storage import StorageService as storage_service
from type_inference.infer import infer_type_of_col
from workers.worker_app import app

logger = get_task_logger(__name__)

@app.task(
    reject_on_worker_lost=True,
)
def infer_data_types_of_chunk(source, part_number, chunk_size, **kwargs):
    file_io = storage_service.download_file(filename=source)
    result = {}
    with pd.read_csv(file_io, iterator=True, chunksize=chunk_size) as iterator:
        chunk = iterator.get_chunk()
        chunk_skip = 0
        while part_number > 0:
            chunk = iterator.get_chunk()
            gc.collect()
            logger.debug(f"Skipping chunk {chunk_skip} of {source}")
            chunk_skip += 1
            part_number -= 1

    for col in chunk.columns:
        t = infer_type_of_col(chunk[col], threshold='auto')
        result[col] = str(t)

    return result
