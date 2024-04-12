from config import BROKER_USER as _user, BROKER_PASSWORD as _password, BROKER_HOST as _host, BROKER_PORT as _port

broker_url = f"pyamqp://{_user}:{_password}@{_host}:{_port}//"
result_backend = 'redis://result-backend:6379/0'

imports = (
    'workers.file_validate',
    'workers.infer_data_types',
    'workers.persist_infer_results',
    'type_inference.tasks',
)

enable_utc = True
