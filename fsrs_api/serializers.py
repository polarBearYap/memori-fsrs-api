from fsrs.models import State as CardState
from rest_framework import serializers

from fsrs_api.models import UserCard


class UserCardSerializer(serializers.ModelSerializer):
    state = serializers.IntegerField()

    class Meta:
        model = UserCard
        fields = [
            "due",
            "stability",
            "difficulty",
            "elapsed_days",
            "scheduled_days",
            "reps",
            "lapses",
            "state",
            "last_review",
            "current_review",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["state"] = CardState(data["state"]).name
        return data

    # def to_internal_value(self, data):
    #     if "state" in data:
    #         data["state"] = CardState[data["state"]].value
    #     return super().to_internal_value(data)

    def to_internal_value(self, data):
        if "state" in data:
            try:
                enum_member = CardState(data["state"])
                data["state"] = enum_member.value
            except ValueError:
                raise serializers.ValidationError({"state": "Invalid state value"})
        return super().to_internal_value(data)
