from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List
from app.db.database import get_async_session
from app.services.offer_service import (
    create_new_offer,
    update_existing_offer,
    get_filtered_offers,
    get_offer_by_id,
    delete_offer_by_id
)
from app.api.schemas.offers import OfferCreate, OfferResponse, OfferUpdate, OfferSearch, OfferIdResponse
from fastapi_pagination import Page

router = APIRouter()


@router.post(
    "/",
    response_model=OfferIdResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new offer",
    description="Create a new offer with categories and optional influencer payouts",
)
async def create_offer(
    payload: OfferCreate,
    db: AsyncSession = Depends(get_async_session),
):
    created = await create_new_offer(db, payload)
   
    return await get_offer_by_id(db, created.id)


@router.patch(
    "/{offer_id}",
    response_model=OfferIdResponse,
    summary="Update an existing offer",
    description="Update offer details by ID",
)
async def update_offer(
    offer_id: UUID,
    payload: OfferUpdate,
    db: AsyncSession = Depends(get_async_session),
):
    updated = await update_existing_offer(db, offer_id, payload)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Offer with ID {offer_id} not found",
        )
    # Return hydrated response with categories and influencers
    return await get_offer_by_id(db, offer_id)


@router.get(
    "/all",
    response_model=Page[OfferResponse],
    summary="Get all offers",
    description="Retrieve paginated list of offers with optional filters",
)
async def get_all_offers(
    db: AsyncSession = Depends(get_async_session),
    params: OfferSearch = Depends(),
):
    offers = await get_filtered_offers(db, params)
    return offers


@router.get(
    "/{offer_id}",
    response_model=OfferIdResponse,
    summary="Get offer by ID",
    description="Retrieve a single offer by its ID",
)
async def get_offer(
    offer_id: UUID,
    db: AsyncSession = Depends(get_async_session),
):

    offer = await get_offer_by_id(db, offer_id)
    if not offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Offer with ID {offer_id} not found",
        )
    return offer


@router.delete(
    "/{offer_id}",
    summary="Delete Offer By ID",
    description="Delete a single offer by its ID",
)
async def delete_offer(offer_id: UUID, db: AsyncSession = Depends(get_async_session)):
    await delete_offer_by_id(db, offer_id)
    return {"mesage":"Offer deleted"}