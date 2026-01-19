"""
Application Configuration
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)
    
    # Application
    APP_NAME: str = "GymBuddy"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite:///./gymbuddy.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


settings = Settings()

