from datetime import datetime

from fsrs.models import SchedulingInfo
from rest_framework import serializers


class DynamicFieldsSerializerMixin:
    def to_representation(self, instance):
        representation = {}
        # Iterate over all attributes of the instance
        for attribute_name in dir(instance):
            attribute_value = getattr(instance, attribute_name, None)
            # Skip private attributes and methods
            if attribute_name.startswith("_") or callable(attribute_value):
                continue
            # Convert datetime to string
            if isinstance(attribute_value, datetime):
                representation[attribute_name] = attribute_value.strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                )
            else:
                representation[attribute_name] = attribute_value
        return representation


class CardSerializer(DynamicFieldsSerializerMixin, serializers.Serializer):
    pass


class ReviewLogSerializer(DynamicFieldsSerializerMixin, serializers.Serializer):
    pass


class SchedulingInfoSerializer(serializers.Serializer):
    card = CardSerializer()
    review_log = ReviewLogSerializer()


class UserCardResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = serializers.SerializerMethodField()

    def get_data(self, obj):
        return {
            key: SchedulingInfoSerializer(value).data for key, value in obj.data.items()
        }


class UserCardResponse:
    def __init__(self, message: str, data: dict[int, SchedulingInfo] = {}):
        self.message = message
        self.data = data

    def serialize(self):
        return UserCardResponseSerializer(self).data
