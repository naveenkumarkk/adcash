"""
Offer API Endpoints
Handles all offer-related HTTP requests
"""

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
)
from app.api.schemas.offers import (
    OfferCreate,
    OfferResponse,
    OfferUpdate,
    OfferSearch,
)
from fastapi_pagination import Page

router = APIRouter()


@router.post(
    "/",
    response_model=OfferResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new offer",
    description="Create a new offer with categories and optional influencer payouts",
)
async def create_offer(
    payload: OfferCreate,
    db: AsyncSession = Depends(get_async_session),
):
    """
    Create a new offer.
    
    Args:
        payload: Offer creation data
        db: Database session
        
    Returns:
        Created offer
    """
    offer = await create_new_offer(db, payload)
    return offer


@router.patch(
    "/{offer_id}",
    response_model=OfferResponse,
    summary="Update an existing offer",
    description="Update offer details by ID",
)
async def update_offer(
    offer_id: UUID,
    payload: OfferUpdate,
    db: AsyncSession = Depends(get_async_session),
):
    """
    Update an existing offer.
    
    Args:
        offer_id: UUID of the offer to update
        payload: Updated offer data
        db: Database session
        
    Returns:
        Updated offer
        
    Raises:
        HTTPException: If offer not found
    """
    offer = await update_existing_offer(db, offer_id, payload)
    if not offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Offer with ID {offer_id} not found",
        )
    return offer


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
    """
    Get all offers with pagination and filters.
    
    Args:
        db: Database session
        params: Search and filter parameters
        
    Returns:
        Paginated list of offers
    """
    offers = await get_filtered_offers(db, params)
    return offers


@router.get(
    "/{offer_id}",
    response_model=OfferResponse,
    summary="Get offer by ID",
    description="Retrieve a single offer by its ID",
)
async def get_offer(
    offer_id: UUID,
    db: AsyncSession = Depends(get_async_session),
):
    """
    Get a single offer by ID.
    
    Args:
        offer_id: UUID of the offer
        db: Database session
        
    Returns:
        Offer details
        
    Raises:
        HTTPException: If offer not found
    """
    offer = await get_offer_by_id(db, offer_id)
    if not offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Offer with ID {offer_id} not found",
        )
    return offer

