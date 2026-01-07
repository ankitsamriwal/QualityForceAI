"""
Application configuration settings
"""
from pydantic_settings import BaseSettings
from typing import List


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

    # AI Configuration
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""

    # Execution Settings
    MAX_CONCURRENT_AGENTS: int = 10
    EXECUTION_TIMEOUT: int = 3600  # 1 hour

    # Database (optional)
    DATABASE_URL: str = "sqlite:///./qualityforce.db"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
