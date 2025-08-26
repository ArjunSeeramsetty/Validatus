import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Core API Keys
    OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "")
    TAVILY_API_KEY: str = os.environ.get("TAVILY_API_KEY", "")
    PERPLEXITY_API_KEY: str = os.environ.get("PERPLEXITY_API_KEY", "")
    PERPLEXITY_DEFAULT_MODEL: str = os.environ.get("PERPLEXITY_DEFAULT_MODEL", "sonar-pro")
    PERPLEXITY_MAX_TOKENS: int = int(os.environ.get("PERPLEXITY_MAX_TOKENS", "2000"))
    
    # Multi-LLM Orchestrator API Keys
    ANTHROPIC_API_KEY: str = os.environ.get('ANTHROPIC_API_KEY', '')
    GOOGLE_GEMINI_API_KEY: str = os.environ.get('GOOGLE_GEMINI_API_KEY', '')
    
    # Infrastructure Configuration
    REDIS_URL: str = os.environ.get("REDIS_URL", "redis://redis:6379")
    DATABASE_URL: str = os.environ.get("DATABASE_URL", "postgresql://postgres:password@postgres:5432/validatus")

    # Knowledge Graph Analyzer Configuration
    NEO4J_URI: str = os.environ.get('NEO4J_URI', 'bolt://localhost:7687')
    NEO4J_USER: str = os.environ.get('NEO4J_USER', 'neo4j')
    NEO4J_PASSWORD: str = os.environ.get('NEO4J_PASSWORD', 'password')

    class Config:
        env_file = ".env"

settings = Settings()
