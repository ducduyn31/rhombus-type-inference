import celery
from celery import states, backends
from celery.backends.redis import RedisBackend
from celery.exceptions import ChordError

import workers.celeryconfig as celeryconfig
from app import settings
from inferstate import autodiscover_callbacks


def patch_celery():
    def _unpack_chord_result(
            self,
            tup,
            decode,
            EXCEPTION_STATES=states.EXCEPTION_STATES,
            PROPAGATE_STATES=states.PROPAGATE_STATES, ):
        _, tid, state, retval = decode(tup)

        if state in EXCEPTION_STATES:
            retval = self.exception_to_python(retval)
        if state in PROPAGATE_STATES:
            return None

        return retval

    backends.redis.RedisBackend._unpack_chord_result = _unpack_chord_result

    return celery


app = patch_celery().Celery(
    main='app',
)

app.config_from_object(celeryconfig)
app.autodiscover_tasks(settings.INSTALLED_APPS, related_name='tasks')
autodiscover_callbacks(settings.INSTALLED_APPS)
