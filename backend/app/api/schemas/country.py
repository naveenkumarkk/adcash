from pydantic import BaseModel

class CountryResponse(BaseModel):
    id:int
    name:str
    code :str
    
    class Config:
        from_attributes=True