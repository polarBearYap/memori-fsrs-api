import logging
import os

from fsrs_core.fsrs_core import FSRSCore
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler

from fsrs_api.models import CardAdapter
from fsrs_api.responses import UserCardResponse
from fsrs_api.serializers import UserCardSerializer

logger = logging.getLogger("django")


@api_view(["POST"])
def user_card_view(request):
    try:
        # Accept JSON data only
        if request.content_type != "application/json":
            resp = UserCardResponse("This view accepts only JSON data.").serialize()
            return Response(
                resp,
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            )
        # To test unknown exception handling
        trigger_exception_for_testing(request)
        # Convert json to UserCard
        serializer = UserCardSerializer(data=request.data)
        # Raise exception if not valid
        serializer.is_valid(raise_exception=True)
        # Convert UserCard (in fsrs_api) to Card (in fsrs)
        card = CardAdapter.adapt_user_card(serializer.validated_data)
        # Get card's next interval and review durations
        fc = FSRSCore()
        scheduled_cards = fc.get_scheduled_cards(
            card, serializer.validated_data["current_review"]
        )
        # Return response
        resp = UserCardResponse(
            "Data validated successfully", scheduled_cards
        ).serialize()
        return Response(resp)

    except ValidationError as e:
        error = f"Validation error: {getattr(e, 'detail', str(e))}"
        logger.error(error)
        resp = UserCardResponse(error).serialize()
        return Response(resp, status=400)

    except Exception as e:
        error = f"Unknown error occurred: {getattr(e, 'detail', str(e))}"
        logger.exception(error)
        resp = UserCardResponse("Unknown error occurred").serialize()
        return Response(
            resp,
            status=500,
        )


def trigger_exception_for_testing(request):
    if os.getenv("TEST_MODE") == "1":
        request.data = None
        raise Exception("Unknown exception triggered")
