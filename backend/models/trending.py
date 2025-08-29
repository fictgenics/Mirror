from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class PlatformType(str, Enum):
    GITHUB = "github"

class GitHubRepo(BaseModel):
    name: str
    full_name: str
    description: Optional[str]
    html_url: str
    stargazers_count: int
    forks_count: int
    language: Optional[str]
    topics: List[str]
    created_at: datetime
    updated_at: datetime
    open_issues_count: int
    contributors_count: Optional[int]
    commits_count: Optional[int]
    tech_stack: List[str]
    stars_per_day: Optional[float] = None
    health_score: Optional[float] = None
    stars_per_contributor: Optional[float] = None




class TrendingTopic(BaseModel):
    topic: str
    query: str
    platforms: List[PlatformType]
    github_data: Optional[List[GitHubRepo]] = []
    analysis_timestamp: datetime = Field(default_factory=datetime.utcnow)
    overall_score: Optional[float] = None

class TrendingAnalysisRequest(BaseModel):
    query: str = Field(..., description="Search query for trending topics")
    platforms: List[PlatformType] = Field(default=[PlatformType.GITHUB])
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
    top_languages: List[Dict[str, Any]]
    top_contributors: List[Dict[str, Any]]
    platform_stats: List[PlatformStats]
