from datetime import datetime
from enum import IntEnum

from fsrs.models import Card, Rating, SchedulingInfo
from fsrs_core.fsrs_core import FSRSCore


def assert_dictionary_keys(dictionary: dict[int, any], enum: IntEnum):
    for key in dictionary.keys():
        assert isinstance(key, enum), f"Key '{key}' is not an instance of the '{enum}'"


def assert_dictionary_values_same_type(dictionary: dict[any, any], expected_type: type):
    for value in dictionary.values():
        assert isinstance(
            value, expected_type
        ), f"Value '{value}' is not of type '{expected_type.__name__}'"


def test_get_scheduled_cards():
    fc = FSRSCore()
    card = Card()
    now = datetime.utcnow()
    scheduling_cards = fc.get_scheduled_cards(card, now)
    assert_dictionary_keys(scheduling_cards, Rating)
    assert_dictionary_values_same_type(scheduling_cards, SchedulingInfo)
