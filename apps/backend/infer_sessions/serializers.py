from django_ulid.models import ULIDField
from django_ulid.serializers import ULIDField as ULIDSerializerField
from rest_framework import serializers

from inferstate import InferStates
from .models import InferSession


class InferSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InferSession
        fields = '__all__'

serializers.ModelSerializer.serializer_field_mapping[ULIDField] = ULIDSerializerField

class InferSessionUpdateSerializer(serializers.Serializer):
    state = serializers.ChoiceField(choices=InferStates.get_choices())
    upload_url = serializers.URLField(required=False)
    filename = serializers.CharField(required=False)

    def validate_state(self, value):
        current_state = self.context["session"].state

        if value == current_state:
            return value

        process = self.context["session"].to_infer_session_process()

        if value == InferStates.INIT:
            raise serializers.ValidationError("Invalid state transition")

        valid_fn = getattr(process, f"may_{value.lower()}")

        if not valid_fn or not valid_fn():
            raise serializers.ValidationError("Invalid state transition")

        return value
