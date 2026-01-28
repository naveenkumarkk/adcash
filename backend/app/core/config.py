from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator, Field
import os


class Settings(BaseSettings):
   
    API_PREFIX: str = Field(default="/api", description="API route prefix")
    DEBUG: bool = Field(default=False, description="Debug mode flag")
    
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:naveenpranesh@localhost:5432/adcash",
        description="Async PostgreSQL database URL"
    )
    ALLOWED_ORIGINS: str = Field(
        default="http://localhost:5173,http://127.0.0.1:5173",
        description="Comma-separated allowed CORS origins"
    )
    
    ENV: str = Field(default="dev", description="Application environment")

    @field_validator("ALLOWED_ORIGINS")
    @classmethod
    def parse_allowed_origins(cls, value: str) -> List[str]:

        if not value:
            return []
        return [origin.strip() for origin in value.split(",")]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore" 


settings = Settings()