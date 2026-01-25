from typing import List, Optional
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel

from app.api.schemas.categories import CategoryResponse
from app.api.schemas.country import CountryResponse
from app.core.enums import PayoutType


class InfluencerPayoutCreate(BaseModel):
    influencer_id: UUID
    custom_amount: Decimal

class OfferCreate(BaseModel):
    title: str
    description: str
    categories: List[int]
    image_url:str|None
    payout_type: PayoutType
    influencer_list:Optional[List[InfluencerPayoutCreate]] = []
    amount:Optional[Decimal] = 0.0


class OfferUpdate(BaseModel):
    id:UUID
    title: Optional[str] = None
    description: Optional[str] = None
    image_url:Optional[str]|None
    categories: Optional[List[int]] = None
    payout: Optional[PayoutType] = None
    country: Optional[int] = None
    amount:Optional[Decimal]

class OfferSearch(BaseModel):
    id:Optional[UUID] = None
    title: Optional[str] = None
    country: Optional[str] = None
    influencer_id: UUID | None = None

class OfferResponse(BaseModel):
    id:UUID
    title:str
    description:str
    image_url:str|None
    categories:List[CategoryResponse]
    payout_type:PayoutType
    country:Optional[str] | None
    amount: Decimal | str

    class Config:
        orm_mode = True

