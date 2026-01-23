from fastapi import APIRouter, Depends,HTTPException
from app.db.database import get_async_session
from typing import List
from app.services.offer_service import (country_list)
from app.api.schemas.country import CountryResponse
from typing import List
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/all",response_model=List[CountryResponse])
async def get_all_endpoint(db:Session=Depends(get_async_session)):
    countries = await country_list(db)
    return countries
