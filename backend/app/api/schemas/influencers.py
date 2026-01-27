from decimal import Decimal
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class InfluencerResponse(BaseModel):
    id: UUID
    name: str
    custom_amount: Optional[Decimal] = None

    model_config = ConfigDict(from_attributes=True)
