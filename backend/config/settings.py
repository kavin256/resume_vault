"""
Application configuration settings.
This module loads environment variables and provides a centralized configuration object.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    # Application Settings
    app_name: str = "Resume Vault"
    env: str = "development"

    # Database Configuration
    database_url: str = "sqlite:///./resume_vault.db"

    # TODO: Cloud Database Integration
    # When migrating to production, update the database_url to point to:
    # - PostgreSQL: postgresql://user:password@host:port/database
    # - MySQL: mysql://user:password@host:port/database
    # - Or use a cloud provider's connection string (AWS RDS, Google Cloud SQL, etc.)

    # AI API Keys (for future resume generation)
    # TODO: Integrate these keys with AI services for resume generation
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    google_ai_api_key: Optional[str] = None

    # Security
    secret_key: str = "your_secret_key_here_change_in_production"

    # CORS Settings
    allowed_origins: str = "http://localhost:3000,http://localhost:8000"

    class Config:
        env_file = ".env"
        case_sensitive = False


# Create a global settings instance
settings = Settings()


def get_settings() -> Settings:
    """
    Dependency function to get settings instance.
    Useful for FastAPI dependency injection.
    """
    return settings
