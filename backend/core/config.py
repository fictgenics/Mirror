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
    
    # Twitter/X API Configuration
    TWITTER_API_KEY: Optional[str] = None
    TWITTER_API_SECRET: Optional[str] = None
    TWITTER_ACCESS_TOKEN: Optional[str] = None
    TWITTER_ACCESS_TOKEN_SECRET: Optional[str] = None
    TWITTER_BEARER_TOKEN: Optional[str] = None
    
    # Reddit API Configuration
    REDDIT_CLIENT_ID: Optional[str] = None
    REDDIT_CLIENT_SECRET: Optional[str] = None
    REDDIT_USER_AGENT: str = "MirrorTrendingAnalyzer/1.0"
    
    # Data Analysis Configuration
    MAX_REPOS_PER_TOPIC: int = 20
    MAX_TWEETS_PER_TOPIC: int = 100
    MAX_REDDIT_POSTS_PER_TOPIC: int = 50
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Create settings instance
settings = Settings()
