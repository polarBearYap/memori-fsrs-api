import copy
import json
import os
import random
from datetime import datetime, timedelta

from fsrs.models import Rating, State
from rest_framework.test import APIClient

now = datetime.utcnow()

BASE_DATA = {
    "due": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
    "stability": random.random(),
    "difficulty": random.random(),
    "elapsed_days": random.randint(1, 5),
    "scheduled_days": random.randint(1, 5),
    "reps": random.randint(1, 5),
    "lapses": random.randint(1, 5),
    "state": random.choice(list(State)).value,
    "last_review": (now - timedelta(days=5)).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "current_review": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
}

URL = "/scheduleusercard"
CONTENT_TYPE = "application/json"


# Validate positive scenario
def test_user_card_view_success():
    client = APIClient()
    data = copy.deepcopy(BASE_DATA)
    response = client.post(URL, json.dumps(data), content_type=CONTENT_TYPE)
    assert response.status_code == 200
    # print(json.dumps(response.data))
    data_keys = response.data["data"].keys()
    expected_keys = set(Rating)
    assert set(data_keys) == expected_keys, "Unexpected keys in response data"

    for rating in Rating:
        assert (
            "card" in response.data["data"][rating]
        ), f"Missing 'card' key for {rating}"
        assert (
            "review_log" in response.data["data"][rating]
        ), f"Missing 'review_log' key for {rating}"
        validate_card_props(response.data["data"][rating]["card"])
        validate_review_log_props(response.data["data"][rating]["review_log"])


def validate_card_props(card_data: dict[str, any]):
    card_props = [
        ("difficulty", [float, int]),
        ("due", [str]),
        ("elapsed_days", [int]),
        ("lapses", [int]),
        ("last_review", [str]),
        ("reps", [int]),
        ("scheduled_days", [int]),
        ("stability", [float, int]),
        ("state", [int]),
    ]
    for prop, prop_type in card_props:
        assert prop in card_data, f"Missing property '{prop}' in card data"
        assert any(
            [isinstance(card_data[prop], curType) for curType in prop_type]
        ), f"Invalid type for '{prop}' in card data"
    validate_datetime_fields(
        card_data,
        [
            "due",
            "last_review",
        ],
    )


def validate_review_log_props(review_log_data: dict[str, any]):
    review_log_props = [
        ("elapsed_days", [int]),
        ("rating", [int]),
        ("review", [str]),
        ("scheduled_days", [int]),
        ("state", [int]),
    ]
    for prop, prop_type in review_log_props:
        assert prop in review_log_data, f"Missing property '{prop}' in review log data"
        assert any(
            [isinstance(review_log_data[prop], curType) for curType in prop_type]
        ), f"Invalid type for '{prop}' in review log data"
    validate_datetime_fields(
        review_log_data,
        [
            "review",
        ],
    )


def validate_datetime_fields(data: dict[str, any], props):
    for prop in props:
        assert (
            is_valid_isoformat(data[prop]) == True
        ), "Invalid iso format for date time field"


def is_valid_isoformat(date_string):
    try:
        datetime.fromisoformat(date_string)
        return True
    except ValueError:
        return False


# Ensure only json is accepted
def test_user_card_view_unaccepted_media():
    client = APIClient()
    data = copy.deepcopy(BASE_DATA)
    response = client.post(URL, data)
    assert response.status_code == 415


# Ensure all fields must not null
def test_user_card_view_validation_error():
    client = APIClient()
    data = copy.deepcopy(BASE_DATA)
    data["due"] = None
    response = client.post(URL, json.dumps(data), content_type=CONTENT_TYPE)
    assert response.status_code == 400


# Ensure the state must be valid
def test_user_card_view_invalid_state():
    client = APIClient()
    data = copy.deepcopy(BASE_DATA)
    data["state"] = 9999
    response = client.post(URL, json.dumps(data), content_type=CONTENT_TYPE)
    assert response.status_code == 400


# Ensure that internal server error is returned as 500
def test_user_card_view_unexpected_error():
    client = APIClient()
    data = None
    os.environ["TEST_MODE"] = "1"
    response = client.post(URL, json.dumps(data), content_type=CONTENT_TYPE)
    assert response.status_code == 500
