from fastapi import APIRouter, Depends,HTTPException
from app.db.database import get_async_session
from typing import List
from app.services.offer_service import (influencer_list)
from app.api.schemas.influencers import InfluencerResponse
from typing import List
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/all",response_model=List[InfluencerResponse])
async def get_all_endpoint(db:Session=Depends(get_async_session)):
    influencers = await influencer_list(db)
    return influencers
