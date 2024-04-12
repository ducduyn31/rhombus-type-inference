from collections import Counter, defaultdict

from celery.utils.log import get_task_logger

from workers.worker_app import app
from infer_sessions.models import InferSession

logger = get_task_logger(__name__)

@app.task
def persist_results(result, session_id, *args, **kwargs):
    session = InferSession.objects.filter(pk=session_id).first()
    if not session:
        return

    result_dict = {} if isinstance(result, list) else result


    if isinstance(result, list):
        infer_results = defaultdict(Counter)


        for r in result:
            if not r:
                continue
            for col, types in r.items():
                infer_results[col].update([types])

        for col, types in infer_results.items():
            result_dict[col] = types.most_common(1)[0]

    parsed_result = {
        "columns_dtypes": {
            col_name: str(dtype[0]) for col_name, dtype in result_dict.items()
        }
    }
    process = session.to_infer_session_process()
    process.trigger('next', result=parsed_result)

