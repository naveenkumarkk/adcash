from typing import List, Optional
from uuid import UUID
from decimal import Decimal
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import NoResultFound
from app.core.enums import PayoutType
from app.db.models.offers import Offer
from app.db.models.categories import Categories
from app.db.models.country import Country
from app.db.models.offer_categories import OfferCategories
from app.db.models.influencer_custom_payouts import InfluencerCustomPayouts
from app.db.models.influencers import Influencers
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.schemas.offers import (
    OfferCreate,
    OfferUpdate,
    OfferSearch,
    OfferResponse,
    CategoryResponse,
)
from sqlalchemy.orm import selectinload
from fastapi_pagination import Page, paginate


async def create_offer(session: AsyncSession, payload: OfferCreate) -> OfferResponse:

    result = await session.execute(select(Offer).where(Offer.title == payload.title))
    offer = result.scalar_one_or_none()

    if not offer:
        offer = Offer(title=payload.title, description=payload.description)
        session.add(offer)
        await session.flush()

    for category_id in payload.categories:
        exists = await session.execute(
            select(OfferCategories).where(
                OfferCategories.offer_id == offer.id,
                OfferCategories.category_id == category_id,
            )
        )
        if not exists.scalar_one_or_none():
            session.add(OfferCategories(offer_id=offer.id, category_id=category_id))

    for ip in payload.influencer_list:
        influencer = await session.execute(
            select(Influencers).where(Influencers.id == ip.influencer_id)
        )
        influencer_info = influencer.scalar_one_or_none()
        if influencer_info:
            exists = await session.execute(
                select(InfluencerCustomPayouts).where(
                    InfluencerCustomPayouts.offer_id == offer.id,
                    InfluencerCustomPayouts.influencer_id == influencer_info.id,
                )
            )
            if not exists.scalar_one_or_none():
                session.add(
                    InfluencerCustomPayouts(
                        offer_id=offer.id,
                        influencer_id=influencer_info.id,
                        amount=ip.custom_amount,
                    )
                )

    await session.commit()
    return offer


def resolve_payout(
    offer: Offer, country: str, influencer_id: Optional[UUID]
) -> tuple[str, Decimal]:

    if influencer_id:
        for cp in offer.influencer_custom_payouts:
            if cp.influencer_id == influencer_id:
                return cp.payout_type, Decimal(cp.amount)

    if not offer.offer_payouts:
        return "N/A", Decimal(0)

    cpa_amounts = [
        p.amount
        for p in offer.offer_payouts
        if p.payout_type == "CPA" and (p.country is None or p.country.code == country)
    ]


def update_offer(db: Session, offer_id: UUID, payload: OfferUpdate):
    return


async def get_all_offer(
    db: AsyncSession,
    params: OfferSearch,
) -> Page[OfferResponse]:
    country = None
    country_cpa_amount = None

    if params.country and params.country != "GLB":
        result = await db.execute(select(Country).where(Country.code == params.country))
        country = result.scalar_one_or_none()
        if country:
            country_cpa_amount = country.cpa_amount

    query = (
        select(Offer)
        .options(
            selectinload(Offer.offer_categories).selectinload(OfferCategories.category)
        )
        .where(Offer.is_active.is_(True))
        .order_by(Offer.id.desc())
    )

    result = await db.execute(query)
    offers = result.scalars().all()

    items: list[OfferResponse] = []

    for offer in offers:
        payout_type = offer.payout_type
        amount = offer.cpa_amount or 0

        if payout_type == PayoutType.FIXED:
            amount = offer.fixed_amount or 0
        elif payout_type == PayoutType.CPA and country_cpa_amount:
            if offer.cpa_amount != country_cpa_amount:
                min_amt = min(offer.cpa_amount, country_cpa_amount)
                max_amt = max(offer.cpa_amount, country_cpa_amount)
                amount = f"{min_amt} - {max_amt}"
        elif payout_type == PayoutType.CPA_FIXED:
            if country_cpa_amount and offer.cpa_amount != country_cpa_amount:
                min_amt = min(offer.cpa_amount, country_cpa_amount)
                max_amt = max(offer.cpa_amount, country_cpa_amount)
                amount = f"{min_amt} - {max_amt} (CPA) + {offer.fixed_amount} (Fixed)"
            else:
                amount = f"{country_cpa_amount or offer.cpa_amount} (CPA) + {offer.fixed_amount} (Fixed)"

        if params.influencer_id:
            result = await db.execute(
                select(InfluencerCustomPayouts).where(
                    InfluencerCustomPayouts.offer_id == offer.id,
                    InfluencerCustomPayouts.influencer_id == params.influencer_id,
                )
            )
            custom = result.scalar_one_or_none()
            if custom:
                amount = f"{custom.amount}"
                payout_type = PayoutType.CUSTOM

        categories_list = [
            CategoryResponse(id=oc.category.id, name=oc.category.name)
            for oc in offer.offer_categories
            if oc.category
        ]

        items.append(
            OfferResponse(
                id=offer.id,
                title=offer.title,
                description=offer.description,
                image_url=offer.image_url,
                categories=categories_list,
                payout_type=payout_type,
                country=country.code if country else None,
                amount=amount,
            )
        )

    return paginate(items)


def get_offer(db: Session, offer_id: UUID):
    return


async def influencer_list(db: Session):
    result = await db.execute(select(Influencers))

    return result.scalars().all()


async def country_list(db: Session):
    result = await db.execute(select(Country))

    return result.scalars().all()
