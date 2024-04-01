from django.db import models
from django.forms import ValidationError
from fsrs.models import Card, State


class UserCard(models.Model):
    due = models.DateTimeField(blank=False)
    stability = models.FloatField(blank=False)
    difficulty = models.FloatField(blank=False)
    elapsed_days = models.IntegerField(blank=False)
    scheduled_days = models.IntegerField(blank=False)
    reps = models.IntegerField(blank=False)
    lapses = models.IntegerField(blank=False)
    state = models.IntegerField(blank=False)
    last_review = models.DateTimeField(blank=False)
    current_review = models.DateTimeField(blank=False)

    def clean(self):
        field_names = self._meta.fields
        # Check if any of the fields are empty
        for field_name in field_names:
            if not getattr(self, field_name):
                raise ValidationError(f"The field {field_name}' must not be null.")
        if not State(self.state) in State:
            raise ValidationError(f"The state value is invalid.")

    def save(self, *args, **kwargs):
        # Validate model fields before saving
        self.full_clean()
        super().save(*args, **kwargs)


class CardAdapter:
    @staticmethod
    def adapt_user_card(user_card_dict: dict[str, any]):
        card = Card()

        card.due = user_card_dict["due"]
        card.stability = user_card_dict["stability"]
        card.difficulty = user_card_dict["difficulty"]
        card.elapsed_days = user_card_dict["elapsed_days"]
        card.scheduled_days = user_card_dict["scheduled_days"]
        card.reps = user_card_dict["reps"]
        card.lapses = user_card_dict["lapses"]
        card.state = user_card_dict["state"]
        card.last_review = user_card_dict["last_review"]

        return card
