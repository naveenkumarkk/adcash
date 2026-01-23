from typing import List,Optional
from uuid import UUID
from decimal import Decimal
from sqlalchemy.orm import Session,joinedload
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
from app.api.schemas.offers import OfferCreate,OfferUpdate,OfferSearch,OfferResponse,CategoryResponse
from sqlalchemy.orm import selectinload

async def create_offer(
    session: AsyncSession,
    payload: OfferCreate
) -> OfferResponse:

    result = await session.execute(
        select(Offer).where(Offer.title == payload.title)
    )
    offer = result.scalar_one_or_none()

    if not offer:
        offer = Offer(
            title=payload.title,
            description=payload.description
        )
        session.add(offer)
        await session.flush() 

    for category_id in payload.categories:
        exists = await session.execute(
            select(OfferCategories).where(
                OfferCategories.offer_id == offer.id,
                OfferCategories.category_id == category_id
            )
        )
        if not exists.scalar_one_or_none():
            session.add(
                OfferCategories(
                    offer_id=offer.id,
                    category_id=category_id
                )
            )

    for ip in payload.influencer_list:
        influencer = await session.execute(
            select(Influencers).where(
                Influencers.id==ip.influencer_id
            )
        )
        influencer_info = influencer.scalar_one_or_none()
        if influencer_info:
            exists = await session.execute(
                select(InfluencerCustomPayouts).where(
                    InfluencerCustomPayouts.offer_id == offer.id,
                    InfluencerCustomPayouts.influencer_id == influencer_info.id
                )
            )
            if not exists.scalar_one_or_none():
                session.add(
                    InfluencerCustomPayouts(
                        offer_id=offer.id,
                        influencer_id=influencer_info.id,
                        amount=ip.custom_amount
                    )
                )

    await session.commit()
    return offer

def resolve_payout(offer:Offer,country:str,influencer_id:Optional[UUID])->tuple[str,Decimal]:
     
    if influencer_id:
        for cp in offer.influencer_custom_payouts:
            if cp.influencer_id == influencer_id:
                return cp.payout_type, Decimal(cp.amount)
    
    if not offer.offer_payouts:
        return "N/A", Decimal(0)
    
    cpa_amounts = [
        p.amount for p in offer.offer_payouts
        if p.payout_type == "CPA" and (p.country is None or p.country.code == country)
    ]

def update_offer(db:Session,offer_id:UUID,payload:OfferUpdate):
    return

async def get_all_offer(db: AsyncSession, params: OfferSearch) -> list[OfferResponse]:
    country = None
    cpa_amount = None

    if params.country and params.country != 'GLB':
        result = await db.execute(
            select(Country).where(Country.code == params.country)
        )
        country = result.scalar_one_or_none()
        if country:
            cpa_amount = country.cpa_amount

    result = await db.execute(
        select(Offer)
        .options(
            selectinload(Offer.offer_categories)
            .selectinload(OfferCategories.category)
        )
        .where(Offer.is_active.is_(True))
    )

    offers = result.scalars().all()
    output = []

    for offer in offers:
        payout_type = offer.payout_type
        amount = f"${offer.amount}"

        if payout_type == PayoutType.CPA and cpa_amount and (offer.amount != cpa_amount):
            amount = f"${min(offer.amount, cpa_amount)} - ${max(offer.amount, cpa_amount)}"
        elif payout_type == PayoutType.CPA_FIXED and cpa_amount :
            if offer.amount != cpa_amount:
                amount = f"${min(offer.amount, cpa_amount)} - ${max(offer.amount, cpa_amount)} (CPA) + {amount} (Fixed)"
            else:
                amount = f"${cpa_amount} (CPA) + {amount} Fixed"

        if params.influencer_id:
            result = await db.execute(
                select(InfluencerCustomPayouts).where(
                    InfluencerCustomPayouts.offer_id == offer.id,
                    InfluencerCustomPayouts.influencer_id == params.influencer_id
                )
            )
            custom = result.scalar_one_or_none()
            if custom:
                amount = f"${custom.amount}"
                payout_type = PayoutType.CUSTOM

        output.append(
            OfferResponse(
                title=offer.title,
                description=offer.description,
                categories=[oc.category for oc in offer.offer_categories],
                payout_type=payout_type,
                country=country.code if country else None,
                amount=amount,
            )
        )

    return output

def get_offer(db:Session,offer_id:UUID):
    return

async def influencer_list(db:Session):
    result = await db.execute(
        select(Influencers)
    )

    return result.scalars().all()

async def country_list(db:Session):
    result = await db.execute(
        select(Country)
    )

    return result.scalars().all()