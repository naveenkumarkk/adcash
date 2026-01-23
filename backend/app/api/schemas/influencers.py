from pydantic import BaseModel
from uuid import UUID
class InfluencerResponse(BaseModel):
    id:UUID
    name:str
    
    class Config:
        from_attributes=True