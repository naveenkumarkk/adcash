"""
Influencer API Endpoints
Handles all influencer-related HTTP requests
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.database import get_async_session
from app.services.influencer_service import get_all_influencers
from app.api.schemas.influencers import InfluencerResponse

router = APIRouter()


@router.get(
    "/all",
    response_model=List[InfluencerResponse],
    summary="Get all influencers",
    description="Retrieve a list of all influencers",
)
async def get_influencers(db: AsyncSession = Depends(get_async_session)):
    """
    Get all influencers.
    
    Args:
        db: Database session
        
    Returns:
        List of all influencers
    """
    influencers = await get_all_influencers(db)
    return influencers
