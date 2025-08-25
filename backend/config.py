import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "")
    TAVILY_API_KEY: str = os.environ.get("TAVILY_API_KEY", "")
    PERPLEXITY_API_KEY: str = os.environ.get("PERPLEXITY_API_KEY", "")
    PERPLEXITY_DEFAULT_MODEL: str = os.environ.get("PERPLEXITY_DEFAULT_MODEL", "sonar-pro")
    PERPLEXITY_MAX_TOKENS: int = int(os.environ.get("PERPLEXITY_MAX_TOKENS", "2000"))
    REDIS_URL: str = os.environ.get("REDIS_URL", "redis://redis:6379")
    DATABASE_URL: str = os.environ.get("DATABASE_URL", "postgresql://postgres:password@postgres:5432/validatus")

    class Config:
        env_file = ".env"

settings = Settings()
