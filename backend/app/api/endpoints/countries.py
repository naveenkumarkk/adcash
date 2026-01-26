"""
Country API Endpoints
Handles all country-related HTTP requests
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.database import get_async_session
from app.services.country_service import get_all_countries
from app.api.schemas.country import CountryResponse

router = APIRouter()


@router.get(
    "/all",
    response_model=List[CountryResponse],
    summary="Get all countries",
    description="Retrieve a list of all countries",
)
async def get_countries(db: AsyncSession = Depends(get_async_session)):
    """
    Get all countries.
    
    Args:
        db: Database session
        
    Returns:
        List of all countries
    """
    countries = await get_all_countries(db)
    return countries
