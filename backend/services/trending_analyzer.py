from typing import List
from datetime import datetime
import asyncio
from concurrent.futures import ThreadPoolExecutor

from models.trending import (
    TrendingTopic, TrendingAnalysisRequest, 
    PlatformType, AnalysisSummary, PlatformStats
)
from services.github_service import GitHubService
from services.nlp_services import SemanticSearch   # 👈 added
from core.config import settings

class TrendingAnalyzer:
    def __init__(self):
        self.github_service = GitHubService()
        self.semantic = SemanticSearch()   # 👈 init Gemini wrapper
    
    async def analyze_trending_topic(self, request: TrendingAnalysisRequest) -> TrendingTopic:
        """Analyze trending topics across all specified platforms"""
        try:
            # Create trending topic object
            trending_topic = TrendingTopic(
                topic=request.query,
                query=request.query,
                platforms=request.platforms,
                analysis_timestamp=datetime.utcnow()
            )
            
            # 🔹 Expand query with NLP (Gemini)
            try:
                expanded_query = await self.semantic.expand_query(request.query)
            except Exception as e:
                print(f"Error expanding query with NLP: {e}")
                expanded_query = request.query  # fallback

            trending_topic.query = expanded_query  # save expanded query
            
            # Collect GitHub data
            if PlatformType.GITHUB in request.platforms:
                try:
                    github_data = await self._collect_github_data(expanded_query, request.max_results_per_platform)
                    trending_topic.github_data = github_data
                except Exception as e:
                    print(f"Error collecting GitHub data: {e}")
                    trending_topic.github_data = []
            
            # Calculate overall score
            trending_topic.overall_score = self._calculate_overall_score(trending_topic)
            
            return trending_topic
            
        except Exception as e:
            print(f"Error in trending analysis: {e}")
            raise
    
    async def _collect_github_data(self, query: str, max_results: int) -> List:
        """Collect GitHub data asynchronously"""
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            return await loop.run_in_executor(
                executor, 
                self.github_service.search_trending_repos, 
                query, 
                max_results
            )
    
    def _calculate_overall_score(self, trending_topic: TrendingTopic) -> float:
        """Calculate overall trending score based on GitHub data"""
        if trending_topic.github_data:
            return self._calculate_github_score(trending_topic.github_data)
        return 0.0
    
    def _calculate_github_score(self, repos: List) -> float:
        """Calculate GitHub trending score"""
        if not repos:
            return 0.0
        
        total_stars = sum(repo.stargazers_count for repo in repos)
        total_forks = sum(repo.forks_count for repo in repos)
        total_contributors = sum(repo.contributors_count or 0 for repo in repos)
        
        # Normalize scores (rough estimates)
        avg_stars = total_stars / len(repos)
        avg_forks = total_forks / len(repos)
        avg_contributors = total_contributors / len(repos)
        
        # Score based on popularity metrics
        score = (avg_stars * 0.5) + (avg_forks * 0.3) + (avg_contributors * 0.2)
        
        # Normalize to 0-100 scale
        return min(score / 1000, 100.0)
    
    def generate_analysis_summary(self, trending_topic: TrendingTopic) -> AnalysisSummary:
        """Generate comprehensive analysis summary"""
        summary = AnalysisSummary(
            total_repos=len(trending_topic.github_data or []),
            top_languages=[],
            top_contributors=[],
            platform_stats=[]
        )
        
        # GitHub analysis
        if trending_topic.github_data:
            summary.top_languages = self.github_service.get_trending_languages(trending_topic.github_data)
            summary.top_contributors = self.github_service.get_top_contributors(trending_topic.github_data)
            
            # GitHub platform stats
            github_stats = PlatformStats(
                platform=PlatformType.GITHUB,
                total_items=len(trending_topic.github_data),
                top_languages=summary.top_languages[:5],
                engagement_metrics={
                    'total_stars': sum(repo.stargazers_count for repo in trending_topic.github_data),
                    'total_forks': sum(repo.forks_count for repo in trending_topic.github_data),
                    'avg_stars': sum(repo.stargazers_count for repo in trending_topic.github_data) / len(trending_topic.github_data)
                },
                trending_keywords=[repo.language for repo in trending_topic.github_data if repo.language]
            )
            summary.platform_stats.append(github_stats)
        
        return summary
