import pytest
from uuid import uuid4
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.offers import Offer
from app.db.models.categories import Categories
from app.db.models.offer_categories import OfferCategories
from app.core.enums import PayoutType
from app.api.schemas.offers import OfferCreate
from app.services.offer_service import create_new_offer, get_offer_by_id
from fastapi.testclient import TestClient


@pytest.mark.asyncio
class TestOfferEndpoints:

    async def test_create_offer(self, client, test_db_session: AsyncSession):
        from app.db.models.categories import Categories
        category = Categories(name="TestCat1")
        test_db_session.add(category)
        await test_db_session.flush()

        payload = {
            "title": "Test Offer Unique123",
            "description": "Test Description",
            "categories": [category.id],
            "image_url": "https://example.com/image.jpg",
            "payout_type": "CPA",
            "cpa_amount": 10.5,
            "fixed_amount": 0,
        }

        response = client.post("/api/offers/", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Offer Unique123"
        assert data["payout_type"] == "CPA"

    async def test_create_offer_with_influencers(
        self, client, test_db_session: AsyncSession
    ):
        from app.db.models.influencers import Influencers

        category = Categories(name="GamingTest")
        test_db_session.add(category)
        await test_db_session.flush()

        inf1 = Influencers(name="InfluencerTest1")
        inf2 = Influencers(name="InfluencerTest2")
        test_db_session.add(inf1)
        test_db_session.add(inf2)
        await test_db_session.flush()

        payload = {
            "title": "Gaming Offer Test456",
            "description": "Gaming promotion",
            "categories": [category.id],
            "image_url": "https://example.com/game.jpg",
            "payout_type": "FIXED",
            "fixed_amount": 25.0,
            "cpa_amount": 0,
            "influencer_list": [
                {"id": str(inf1.id), "name": "InfluencerTest1", "custom_amount": 50},
                {"id": str(inf2.id), "name": "InfluencerTest2", "custom_amount": 75},
            ],
        }

        response = client.post("/api/offers/", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Gaming Offer Test456"
        assert len(data["influencer_list"]) == 2

    async def test_get_offer_by_id(self, client, test_db_session: AsyncSession):
        category = Categories(name="Fashion")
        test_db_session.add(category)
        await test_db_session.flush()
        offer = Offer(
            title="Fashion Offer",
            description="Fashion promotion",
            payout_type=PayoutType.CPA,
            cpa_amount=15.0,
            fixed_amount=0,
        )
        test_db_session.add(offer)
        await test_db_session.flush()

        oc = OfferCategories(offer_id=offer.id, category_id=category.id)
        test_db_session.add(oc)
        await test_db_session.commit()

        response = client.get(f"/api/offers/{offer.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(offer.id)
        assert data["title"] == "Fashion Offer"
        assert len(data["categories"]) == 1

    async def test_get_offer_not_found(self, client):
        fake_id = uuid4()
        response = client.get(f"/api/offers/{fake_id}")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    async def test_update_offer(self, client, test_db_session: AsyncSession):
        category = Categories(name="HealthTest")
        test_db_session.add(category)
        await test_db_session.flush()
        offer = Offer(
            title="Health Offer Test",
            description="Original description",
            payout_type=PayoutType.FIXED,
            cpa_amount=0,
            fixed_amount=20.0,
        )
        test_db_session.add(offer)
        await test_db_session.flush()

        oc = OfferCategories(offer_id=offer.id, category_id=category.id)
        test_db_session.add(oc)
        await test_db_session.commit()

        payload = {
            "id": str(offer.id),
            "title": "Updated Health Offer",
            "description": "Updated description",
            "image_url": None,
            "cpa_amount": 0,
            "fixed_amount": 25.0,
        }

        response = client.patch(f"/api/offers/{offer.id}", json=payload)
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["title"] == "Updated Health Offer"
        assert data["description"] == "Updated description"

    async def test_delete_offer(self, client, test_db_session: AsyncSession):
        offer = Offer(
            title="Delete Me",
            description="This will be deleted",
            payout_type=PayoutType.CPA,
            cpa_amount=10.0,
            fixed_amount=0,
        )
        test_db_session.add(offer)
        await test_db_session.commit()

        response = client.delete(f"/api/offers/{offer.id}")
        assert response.status_code == 200
        response = client.get(f"/api/offers/{offer.id}")
        assert response.status_code == 404

    async def test_get_all_offers(self, client, test_db_session: AsyncSession):
        for i in range(3):
            offer = Offer(
                title=f"Offer {i}",
                description=f"Description {i}",
                payout_type=PayoutType.CPA,
                cpa_amount=10.0 + i,
                fixed_amount=0,
            )
            test_db_session.add(offer)
        await test_db_session.commit()

        response = client.get("/api/offers/all")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) > 0

    async def test_get_offers_by_title(self, client, test_db_session: AsyncSession):

        offer1 = Offer(
            title="Tech Offer",
            description="Tech description",
            payout_type=PayoutType.CPA,
            cpa_amount=15.0,
            fixed_amount=0,
        )
        offer2 = Offer(
            title="Finance Offer",
            description="Finance description",
            payout_type=PayoutType.CPA_FIXED,
            cpa_amount=20.0,
            fixed_amount=5.0,
        )
        test_db_session.add(offer1)
        test_db_session.add(offer2)
        await test_db_session.commit()

        response = client.get("/api/offers/all?title=Tech")
        assert response.status_code == 200
        data = response.json()
        items = data["items"]
        assert len(items) > 0
        assert any("Tech" in item["title"] for item in items)

    async def test_offer_cpa_fixed_payout(self, client, test_db_session: AsyncSession):
        category = Categories(name="FinanceTest")
        test_db_session.add(category)
        await test_db_session.flush()

        payload = {
            "title": "CPA Fixed Offer Test789",
            "description": "Both CPA and fixed",
            "categories": [category.id],
            "image_url": "https://example.com/finance.jpg",
            "payout_type": "CPA_FIXED",
            "cpa_amount": 20.0,
            "fixed_amount": 10.0,
        }

        response = client.post("/api/offers/", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["payout_type"] == "CPA_FIXED"

    async def test_offer_inactive_not_in_list(self, client, test_db_session: AsyncSession):
        offer = Offer(
            title="Inactive Offer",
            description="This is inactive",
            payout_type=PayoutType.CPA,
            cpa_amount=10.0,
            fixed_amount=0,
            is_active=False,
        )
        test_db_session.add(offer)
        await test_db_session.commit()

        response = client.get("/api/offers/all")
        assert response.status_code == 200
        data = response.json()
        titles = [item["title"] for item in data["items"]]
        assert "Inactive Offer" not in titles
