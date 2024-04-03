from celery import Celery
import workers.celeryconfig as celeryconfig

app = Celery(
    main='app',
)

app.config_from_object(celeryconfig)