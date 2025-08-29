from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # App Configuration
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # GitHub API Configuration
    GITHUB_TOKEN: Optional[str] = None
    

    
    # Data Analysis Configuration
    MAX_REPOS_PER_TOPIC: int = 20
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Create settings instance
settings = Settings()
