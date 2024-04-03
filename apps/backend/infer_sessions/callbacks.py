
def save_model_on_state_updated(session_machine, *args, **kwargs):
    from infer_sessions.models import InferSession

    current_state = session_machine.state
    model = InferSession.objects.get(session_id=session_machine.session_id)
    model.state = current_state

    for key in kwargs:
        if hasattr(model, key):
            setattr(model, key, kwargs[key])

    model.save()

def move_next_state_automatically(session_machine, *args, **kwargs):
    from infer_sessions.models import InferSession

    model = InferSession.objects.filter(pk=session_machine.session_id).first()
    if not model:
        return
    process = model.to_infer_session_process()
    process.trigger("next",)

def dispatch_workers_to_validate_file(session_machine, *args, **kwargs):
    from workers.file_validate import validate_file

    validate_file.delay(str(session_machine.session_id), *args, **kwargs)

def dispatch_workers_to_infer_types(session_machine, *args, **kwargs):
    from workers.infer_data_types import infer_data_types

    infer_data_types.delay(str(session_machine.session_id), *args, **kwargs)