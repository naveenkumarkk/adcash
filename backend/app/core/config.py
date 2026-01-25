from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator
import os

class Settings(BaseSettings):
    API_PREFIX:str = "/api"
    DEBUG:bool = False
    #postgresql+asyncpg://<username>:<password>@<host>:<port>/<database>

    DATABASE_URL:str="postgresql+asyncpg://postgres:naveenpranesh@localhost:5432/adcash"
    ALLOWED_ORIGINS:str="http://localhost:5732,http://localhost:5733,http://localhost:3000,http://localhost:3001"
    ENV: str = "dev" 

    def __init__(self,**values):
        super().__init__(**values)

    @field_validator("ALLOWED_ORIGINS")
    def parse_allowed_origins(cls,v:str) -> List[str]:
        return v.split(",") if v else []
    
    class Config:
        env_file = ".env"
        env_file_encoding="utf-8"
        case_sensitive=True

settings = Settings()