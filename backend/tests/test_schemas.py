import pytest
from uuid import uuid4
from decimal import Decimal
from app.api.schemas.offers import OfferCreate, OfferResponse, OfferIdResponse
from app.core.enums import PayoutType


class TestOfferSchemas:

    def test_offer_create_valid(self):
        offer = OfferCreate(
            title="Test Offer",
            description="Test Description",
            categories=[1, 2],
            image_url="https://example.com/image.jpg",
            payout_type=PayoutType.CPA,
            cpa_amount=Decimal("10.0"),
            fixed_amount=Decimal("5.0"),
        )
        assert offer.title == "Test Offer"
        assert offer.cpa_amount == Decimal("10.0")

    def test_offer_create_minimal(self):
        offer = OfferCreate(
            title="Test Offer",
            description="Test Description",
            categories=[1],
            image_url=None,
            payout_type=PayoutType.FIXED,
        )
        assert offer.title == "Test Offer"
        assert offer.cpa_amount == 0.0
        assert offer.fixed_amount == 0.0
