"""
Application configuration settings
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings"""

    # API Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ]

    # Storage
    RESULTS_DIR: str = "test_results"
    EVIDENCE_DIR: str = "test_evidences"

    # AI Configuration (OPTIONAL - agents work without these)
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""

    # Execution Settings
    MAX_CONCURRENT_AGENTS: int = 10
    EXECUTION_TIMEOUT: int = 3600  # 1 hour

    # Database (optional)
    DATABASE_URL: str = "sqlite:///./qualityforce.db"

    # Feature flags
    USE_AI_GENERATION: bool = False  # Set to True if you have API keys configured

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields in .env


settings = Settings()

# Create storage directories if they don't exist
os.makedirs(settings.RESULTS_DIR, exist_ok=True)
os.makedirs(settings.EVIDENCE_DIR, exist_ok=True)
