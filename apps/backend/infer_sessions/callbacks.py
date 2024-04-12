from inferstate import callback, InferStates
from django_eventstream import send_event


@callback()
def save_model_on_state_updated(session_machine, *args, **kwargs):
    from infer_sessions.models import InferSession

    current_state = session_machine.state
    model = InferSession.objects.get(session_id=session_machine.session_id)
    model.state = current_state

    for key in kwargs:
        if hasattr(model, key):
            setattr(model, key, kwargs[key])

    model.save()


@callback()
def publish_sse_on_state_updated(session_machine, *args, **kwargs):
    session_id = str(session_machine.session_id)
    current_state = str(session_machine.state)
    send_event(f"session-{session_id}", "message", {
        "session_id": session_id,
        "state": current_state,
    })


@callback(states=[InferStates.FILE_UPLOADED])
def move_next_state_automatically(session_machine, *args, **kwargs):
    from infer_sessions.models import InferSession

    model = InferSession.objects.filter(pk=session_machine.session_id).first()
    if not model:
        return
    process = model.to_infer_session_process()
    process.trigger("next", )


@callback(states=[InferStates.VALIDATE_FILE])
def dispatch_workers_to_validate_file(session_machine, *args, **kwargs):
    from workers.file_validate import validate_file

    validate_file.delay(str(session_machine.session_id), *args, **kwargs)


@callback(states=[InferStates.INFER_FILE])
def dispatch_workers_to_infer_types(session_machine, *args, **kwargs):
    from workers.infer_data_types import infer_data_types, on_infer_data_error

    infer_data_types.delay(str(session_machine.session_id), reject_on_worker_lost=True,
                           link_error=on_infer_data_error.s(str(session_machine.session_id)), *args, **kwargs)
