from config import BROKER_USER as _user, BROKER_PASSWORD as _password, BROKER_HOST as _host, BROKER_PORT as _port

broker_url = f"pyamqp://{_user}:{_password}@{_host}:{_port}//"

imports = (
    'workers.file_validate',
    'workers.infer_data_types',
    'type_inference.tasks',
)

enable_utc = True
