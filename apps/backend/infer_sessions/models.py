from auditlog.registry import auditlog
from django.db import models, connection as db_conn
from django_ulid.models import default, ULIDField

from inferstate import InferSessionProcess, InferStates


# Create your models here.
class InferSession(models.Model):
    session_id = ULIDField(default=default, primary_key=True, editable=False)
    state = models.CharField(max_length=255, choices=InferStates.get_choices(), default=InferStates.INIT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    file = models.CharField(max_length=255, null=True, blank=True)
    result = models.JSONField(null=True, blank=True)
    error = models.JSONField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.session_id} - {self.state}"

    def to_infer_session_process(self):
        return InferSessionProcess(
            session_id=self.session_id,
            state=self.state,
        )


def get_internal_type(self):
    return 'UUIDField' if db_conn.features.has_native_uuid_field else 'CharField'


ULIDField.get_internal_type = get_internal_type

auditlog.register(InferSession)
