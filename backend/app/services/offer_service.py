from typing import List, Optional
from uuid import UUID
from decimal import Decimal
from app.core.enums import PayoutType
from app.db.models.offers import Offer
from app.db.models.categories import Categories
from app.db.models.country import Country
from app.db.models.offer_categories import OfferCategories
from app.db.models.influencer_custom_payouts import InfluencerCustomPayouts
from app.db.models.influencers import Influencers
from app.api.schemas.offers import (
    OfferCreate,
    OfferUpdate,
    OfferSearch,
    OfferResponse,
    CategoryResponse,
    OfferIdResponse,
    InfluencerResponse
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from fastapi_pagination import Page, paginate


async def create_new_offer(
    db_session: AsyncSession, payload: OfferCreate
) -> Offer:
    result = await db_session.execute(select(Offer).where(Offer.title == payload.title))
    offer = result.scalar_one_or_none()

    if not offer:
        offer = Offer(
            title=payload.title,
            description=payload.description,
            cpa_amount=payload.cpa_amount,
            fixed_amount=payload.fixed_amount,
            payout_type=payload.payout_type,
        )
        db_session.add(offer)
        await db_session.flush()

    await _add_offer_categories(db_session, offer.id, payload.categories)

    if payload.influencer_list:
        await _add_influencer_payouts(db_session, offer.id, payload.influencer_list)

    await db_session.commit()
    await db_session.flush()
    return offer


async def _add_offer_categories(
    db_session: AsyncSession, offer_id: UUID, category_ids: List[int]
) -> None:
    for category_id in category_ids:
        exists = await db_session.execute(
            select(OfferCategories).where(
                OfferCategories.offer_id == offer_id,
                OfferCategories.category_id == category_id,
            )
        )
        if not exists.scalar_one_or_none():
            db_session.add(OfferCategories(offer_id=offer_id, category_id=category_id))


async def _update_offer_categories(
    db_session: AsyncSession, offer_id: UUID, category_ids: List[int]
):
    await db_session.execute(
        delete(OfferCategories).where(OfferCategories.offer_id == offer_id)
    )

    await _add_offer_categories(db_session, offer_id, category_ids)


async def _update_influencer_offer(
    db_session: AsyncSession, offer_id: UUID, influencer_payouts: List
):
    await db_session.execute(
        delete(InfluencerCustomPayouts).where(
            InfluencerCustomPayouts.offer_id == offer_id
        )
    )

    for payout_data in influencer_payouts:
        if not payout_data.id:
            continue
        influencer = await db_session.execute(
            select(Influencers).where(Influencers.id == payout_data.id)
        )
        influencer_info = influencer.scalar_one_or_none()

        if influencer_info:
            db_session.add(
                InfluencerCustomPayouts(
                    offer_id=offer_id,
                    influencer_id=influencer_info.id,
                    amount=payout_data.custom_amount,
                )
            )


async def _add_influencer_payouts(
    db_session: AsyncSession, offer_id: UUID, influencer_payouts: List
) -> None:
    for payout_data in influencer_payouts:
        influencer = await db_session.execute(
            select(Influencers).where(Influencers.id == payout_data.id)
        )
        influencer_info = influencer.scalar_one_or_none()

        if influencer_info:
            exists = await db_session.execute(
                select(InfluencerCustomPayouts).where(
                    InfluencerCustomPayouts.offer_id == offer_id,
                    InfluencerCustomPayouts.influencer_id == influencer_info.id,
                )
            )
            if not exists.scalar_one_or_none():
                db_session.add(
                    InfluencerCustomPayouts(
                        offer_id=offer_id,
                        influencer_id=influencer_info.id,
                        amount=payout_data.custom_amount,
                    )
                )


async def update_existing_offer(
    db_session: AsyncSession, offer_id: UUID, payload: OfferUpdate
) -> Optional[OfferResponse]:

    result = await db_session.execute(select(Offer).where(Offer.id == offer_id))
    offer = result.scalar_one_or_none()

    if not offer:
        return None

    if payload.title is not None:
        offer.title = payload.title
    if payload.description is not None:
        offer.description = payload.description
    if payload.image_url is not None:
        offer.image_url = payload.image_url
    if payload.payout_type is not None:
        offer.payout_type = payload.payout_type
    if payload.cpa_amount is not None:
        offer.cpa_amount = float(payload.cpa_amount)
    if payload.fixed_amount is not None:
        offer.fixed_amount = float(payload.fixed_amount)
    if payload.influencer_list:
        await _update_influencer_offer(db_session, offer.id, payload.influencer_list)
    if payload.categories:
        await _update_offer_categories(db_session, offer.id, payload.categories)

    await db_session.commit()
    await db_session.refresh(offer)
    return offer


async def get_filtered_offers(
    db_session: AsyncSession,
    params: OfferSearch,
) -> Page[OfferResponse]:
    country = None
    country_cpa_amount = None

    if params.country:
        result = await db_session.execute(
            select(Country).where(Country.id == params.country)
        )
        country = result.scalar_one_or_none()
        if country and country.code != "GLB":
            country_cpa_amount = country.cpa_amount

    query = (
        select(Offer)
        .options(
            selectinload(Offer.offer_categories).selectinload(OfferCategories.category)
        )
        .where(Offer.is_active.is_(True))
        .order_by(Offer.id.desc())
    )

    if params.title:
        query = query.where(Offer.title.ilike(f"%{params.title}%"))

    result = await db_session.execute(query)
    offers = result.scalars().all()

    items = []
    for offer in offers:
        payout_type = offer.payout_type
        amount = _calculate_offer_amount(offer, payout_type, country_cpa_amount)

        if params.influencer_id:
            custom_amount, custom_payout = await _get_custom_influencer_payout(
                db_session, offer.id, params.influencer_id
            )
            if custom_amount:
                amount = custom_amount
                payout_type = custom_payout

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


def _calculate_offer_amount(
    offer: Offer,
    payout_type: PayoutType,
    country_cpa_amount: Optional[float],
) -> str:
    if payout_type == PayoutType.FIXED:
        return f"${offer.fixed_amount or 0}"

    if payout_type == PayoutType.CPA:
        if country_cpa_amount and offer.cpa_amount != country_cpa_amount:
            min_amt = min(offer.cpa_amount, country_cpa_amount)
            max_amt = max(offer.cpa_amount, country_cpa_amount)
            return f"${min_amt} - ${max_amt}"
        return f"${offer.cpa_amount or 0}"

    if payout_type == PayoutType.CPA_FIXED:
        cpa_part = country_cpa_amount or offer.cpa_amount
        if country_cpa_amount and offer.cpa_amount != country_cpa_amount:
            min_amt = min(offer.cpa_amount, country_cpa_amount)
            max_amt = max(offer.cpa_amount, country_cpa_amount)
            return f"${min_amt} - ${max_amt} (CPA) + ${offer.fixed_amount} (Fixed)"
        return f"${cpa_part} (CPA) + ${offer.fixed_amount} (Fixed)"

    return f"${offer.cpa_amount or 0}"


async def _get_custom_influencer_payout(
    db_session: AsyncSession, offer_id: UUID, influencer_id: UUID
) -> tuple[Optional[str], Optional[PayoutType]]:

    result = await db_session.execute(
        select(InfluencerCustomPayouts).where(
            InfluencerCustomPayouts.offer_id == offer_id,
            InfluencerCustomPayouts.influencer_id == influencer_id,
        )
    )
    custom = result.scalar_one_or_none()

    if custom:
        return f"${custom.amount}", PayoutType.CUSTOM
    return None, None


async def get_offer_by_id(
    db_session: AsyncSession,
    offer_id: UUID,
) -> OfferIdResponse | None:

    query = (
        select(Offer)
        .options(
            selectinload(Offer.offer_categories)
                .selectinload(OfferCategories.category),
            selectinload(Offer.influencer_custom_payouts)
                .selectinload(InfluencerCustomPayouts.influencer),
        )
        .where(
            Offer.id == offer_id,
            Offer.is_active.is_(True),
        )
    )

    result = await db_session.execute(query)
    offer = result.scalar_one_or_none()

    if not offer:
        return None

    categories = [
        CategoryResponse(
            id=oc.category.id,
            name=oc.category.name,
        )
        for oc in offer.offer_categories
        if oc.category
    ]

    influencer_list = [
        InfluencerResponse(
            id=icp.influencer.id,
            name=icp.influencer.name,
            custom_amount=icp.amount,
        )
        for icp in offer.influencer_custom_payouts
        if icp.influencer
    ]

    return OfferIdResponse(
        id=offer.id,
        title=offer.title,
        description=offer.description,
        image_url=offer.image_url,
        categories=categories,
        payout_type=offer.payout_type,
        cpa_amount=Decimal(str(offer.cpa_amount or 0)),
        fixed_amount=Decimal(str(offer.fixed_amount or 0)),
        influencer_list=influencer_list,
    )


async def delete_offer_by_id(
    db_session: AsyncSession,
    offer_id: UUID,
):
    async with db_session.begin():  
        await db_session.execute(
            delete(OfferCategories).where(
                OfferCategories.offer_id == offer_id
            )
        )

        await db_session.execute(
            delete(InfluencerCustomPayouts).where(
                InfluencerCustomPayouts.offer_id == offer_id
            )
        )

        await db_session.execute(
            delete(Offer).where(
                Offer.id == offer_id 
            )
        )