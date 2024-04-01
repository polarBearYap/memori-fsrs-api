from datetime import datetime

from fsrs import FSRS
from fsrs.models import Card, Rating, SchedulingInfo


class FSRSCore:
    def __init__(self):
        self.fsrs = FSRS()

    def get_scheduled_cards(
        self, card: Card, review_date_time: datetime
    ) -> dict[Rating, SchedulingInfo]:
        scheduling_cards = self.fsrs.repeat(card, review_date_time)
        return scheduling_cards
