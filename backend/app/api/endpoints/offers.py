from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_async_session
from uuid import UUID
from app.services.offer_service import (create_offer,update_offer,get_all_offer,get_offer)
from app.api.schemas.offers import (OfferCreate,OfferResponse,OfferUpdate,OfferSearch)
from typing import List
from fastapi_pagination import Page

router = APIRouter()

@router.post("/",response_model=OfferResponse)
async def create_offer_endpoint(payload:OfferCreate,db:Session=Depends(get_async_session)):
    offer = await create_offer(db,payload)
    return offer

@router.patch("/{offer_id}",response_model=OfferResponse)
def update_offer_endpoint(offer_id:UUID,payload:OfferUpdate,db:Session=Depends(get_async_session)):
    offer = update_offer(db,offer_id,payload)
    return offer


@router.get("/all", response_model=Page[OfferResponse])
async def get_all_endpoint(
    db: Session = Depends(get_async_session),
    params: OfferSearch = Depends()
):
    offers = await get_all_offer(db, params)
    return offers

@router.get("/{offer_id}",response_model=List[OfferResponse])
def get_offer_endpoint(offer_id:UUID,db:Session=Depends(get_async_session)):
    offers = get_offer(db,offer_id)
    return {"success": True, "message": "Offer deleted successfully"}

