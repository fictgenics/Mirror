from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class PlatformType(str, Enum):
    GITHUB = "github"
    TWITTER = "twitter"
    REDDIT = "reddit"

class GitHubRepo(BaseModel):
    name: str
    full_name: str
    description: Optional[str]
    html_url: str
    stargazers_count: int
    forks_count: int
    language: Optional[str]
    topics: List[str] = []
    created_at: datetime
    updated_at: datetime
    open_issues_count: int
    contributors_count: Optional[int]
    commits_count: Optional[int]
    tech_stack: List[str] = []

class TwitterPost(BaseModel):
    id: str
    text: str
    author_id: str
    author_username: str
    created_at: datetime
    retweet_count: int
    like_count: int
    reply_count: int
    quote_count: int
    hashtags: List[str] = []
    mentions: List[str] = []

class RedditPost(BaseModel):
    id: str
    title: str
    selftext: str
    author: str
    subreddit: str
    score: int
    upvote_ratio: float
    num_comments: int
    created_utc: datetime
    url: str
    is_self: bool
    domain: str

class TrendingTopic(BaseModel):
    topic: str
    query: str
    platforms: List[PlatformType]
    github_data: Optional[List[GitHubRepo]] = []
    twitter_data: Optional[List[TwitterPost]] = []
    reddit_data: Optional[List[RedditPost]] = []
    analysis_timestamp: datetime = Field(default_factory=datetime.utcnow)
    overall_score: Optional[float] = None

class TrendingAnalysisRequest(BaseModel):
    query: str = Field(..., description="Search query for trending topics")
    platforms: List[PlatformType] = Field(default=[PlatformType.GITHUB, PlatformType.TWITTER, PlatformType.REDDIT])
    max_results_per_platform: int = Field(default=20, ge=1, le=100)

class TrendingAnalysisResponse(BaseModel):
    success: bool
    message: str
    data: Optional[TrendingTopic] = None
    error: Optional[str] = None

class PlatformStats(BaseModel):
    platform: PlatformType
    total_items: int
    top_languages: List[Dict[str, Any]] = []
    engagement_metrics: Dict[str, Any] = {}
    trending_keywords: List[str] = []

class AnalysisSummary(BaseModel):
    total_repos: int
    total_tweets: int
    total_reddit_posts: int
    top_languages: List[Dict[str, Any]]
    top_contributors: List[Dict[str, Any]]
    engagement_trends: Dict[str, Any]
    platform_stats: List[PlatformStats]
