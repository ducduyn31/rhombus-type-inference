from celery import Celery
import workers.celeryconfig as celeryconfig
from app import settings
from inferstate import autodiscover_callbacks

app = Celery(
    main='app',
)

app.config_from_object(celeryconfig)
app.autodiscover_tasks(settings.INSTALLED_APPS, related_name='tasks')
autodiscover_callbacks(settings.INSTALLED_APPS)
