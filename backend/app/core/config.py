"""
Application Configuration
Manages all application settings and environment variables
"""

from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator, Field
import os


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Attributes:
        API_PREFIX: Prefix for all API routes
        DEBUG: Enable debug mode
        DATABASE_URL: PostgreSQL connection string
        ALLOWED_ORIGINS: Comma-separated list of allowed CORS origins
        ENV: Current environment (dev, staging, production)
    """
    
    # API Configuration
    API_PREFIX: str = Field(default="/api", description="API route prefix")
    DEBUG: bool = Field(default=False, description="Debug mode flag")
    
    # Database Configuration
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:naveenpranesh@localhost:5432/adcash",
        description="Async PostgreSQL database URL"
    )
    
    # CORS Configuration
    ALLOWED_ORIGINS: str = Field(
        default="http://localhost:5173,http://127.0.0.1:5173",
        description="Comma-separated allowed CORS origins"
    )
    
    # Environment
    ENV: str = Field(default="dev", description="Application environment")

    @field_validator("ALLOWED_ORIGINS")
    @classmethod
    def parse_allowed_origins(cls, value: str) -> List[str]:
        """
        Parse comma-separated origins string into a list.
        
        Args:
            value: Comma-separated string of origins
            
        Returns:
            List of origin URLs
        """
        if not value:
            return []
        return [origin.strip() for origin in value.split(",")]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields


# Global settings instance
settings = Settings()