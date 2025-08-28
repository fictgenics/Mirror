from typing import List, Dict, Any, Optional
from datetime import datetime
import asyncio
from concurrent.futures import ThreadPoolExecutor

from models.trending import (
    TrendingTopic, TrendingAnalysisRequest, 
    PlatformType, AnalysisSummary, PlatformStats
)
from services.github_service import GitHubService
from services.twitter_service import TwitterService
from services.reddit_service import RedditService
from core.config import settings

class TrendingAnalyzer:
    def __init__(self):
        self.github_service = GitHubService()
        self.twitter_service = TwitterService()
        self.reddit_service = RedditService()
    
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
            
            # Collect data from all platforms concurrently
            tasks = []
            
            if PlatformType.GITHUB in request.platforms:
                tasks.append(self._collect_github_data(request.query, request.max_results_per_platform))
            
            if PlatformType.TWITTER in request.platforms:
                tasks.append(self._collect_twitter_data(request.query, request.max_results_per_platform))
            
            if PlatformType.REDDIT in request.platforms:
                tasks.append(self._collect_reddit_data(request.query, request.max_results_per_platform))
            
            # Execute all tasks concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    print(f"Error collecting data from platform {i}: {result}")
                    continue
                
                if PlatformType.GITHUB in request.platforms and i == 0:
                    trending_topic.github_data = result
                elif PlatformType.TWITTER in request.platforms and i == 1:
                    trending_topic.twitter_data = result
                elif PlatformType.REDDIT in request.platforms and i == 2:
                    trending_topic.reddit_data = result
            
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
    
    async def _collect_twitter_data(self, query: str, max_results: int) -> List:
        """Collect Twitter data asynchronously"""
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            return await loop.run_in_executor(
                executor, 
                self.twitter_service.search_trending_posts, 
                query, 
                max_results
            )
    
    async def _collect_reddit_data(self, query: str, max_results: int) -> List:
        """Collect Reddit data asynchronously"""
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            return await loop.run_in_executor(
                executor, 
                self.reddit_service.search_trending_posts, 
                query, 
                max_results
            )
    
    def _calculate_overall_score(self, trending_topic: TrendingTopic) -> float:
        """Calculate overall trending score based on all platform data"""
        score = 0.0
        total_weight = 0.0
        
        # GitHub scoring (weight: 0.4)
        if trending_topic.github_data:
            github_score = self._calculate_github_score(trending_topic.github_data)
            score += github_score * 0.4
            total_weight += 0.4
        
        # Twitter scoring (weight: 0.35)
        if trending_topic.twitter_data:
            twitter_score = self._calculate_twitter_score(trending_topic.twitter_data)
            score += twitter_score * 0.35
            total_weight += 0.35
        
        # Reddit scoring (weight: 0.25)
        if trending_topic.reddit_data:
            reddit_score = self._calculate_reddit_score(trending_topic.reddit_data)
            score += reddit_score * 0.25
            total_weight += 0.25
        
        # Normalize score
        if total_weight > 0:
            return score / total_weight
        return 0.0
    
    def _calculate_github_score(self, repos: List) -> float:
        """Calculate GitHub trending score"""
        if not repos:
            return 0.0
        
        total_stars = sum(repo.stargazers_count for repo in repos)
        total_forks = sum(repo.forks_count for repo in repos)
        total_contributors = sum(repo.contributors_count or 0 for repo in repos)
        
        # Normalize scores (these are rough estimates)
        avg_stars = total_stars / len(repos)
        avg_forks = total_forks / len(repos)
        avg_contributors = total_contributors / len(repos)
        
        # Score based on popularity metrics
        score = (avg_stars * 0.5) + (avg_forks * 0.3) + (avg_contributors * 0.2)
        
        # Normalize to 0-100 scale
        return min(score / 1000, 100.0)
    
    def _calculate_twitter_score(self, posts: List) -> float:
        """Calculate Twitter trending score"""
        if not posts:
            return 0.0
        
        total_likes = sum(post.like_count for post in posts)
        total_retweets = sum(post.retweet_count for post in posts)
        total_replies = sum(post.reply_count for post in posts)
        
        # Calculate engagement rate
        total_engagement = total_likes + total_retweets + total_replies
        avg_engagement = total_engagement / len(posts)
        
        # Normalize to 0-100 scale
        return min(avg_engagement / 100, 100.0)
    
    def _calculate_reddit_score(self, posts: List) -> float:
        """Calculate Reddit trending score"""
        if not posts:
            return 0.0
        
        total_score = sum(post.score for post in posts)
        total_comments = sum(post.num_comments for post in posts)
        
        # Calculate average engagement
        avg_score = total_score / len(posts)
        avg_comments = total_comments / len(posts)
        
        # Score based on upvotes and comments
        score = (avg_score * 0.7) + (avg_comments * 0.3)
        
        # Normalize to 0-100 scale
        return min(score / 100, 100.0)
    
    def generate_analysis_summary(self, trending_topic: TrendingTopic) -> AnalysisSummary:
        """Generate comprehensive analysis summary"""
        summary = AnalysisSummary(
            total_repos=len(trending_topic.github_data or []),
            total_tweets=len(trending_topic.twitter_data or []),
            total_reddit_posts=len(trending_topic.reddit_data or []),
            top_languages=[],
            top_contributors=[],
            engagement_trends={},
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
        
        # Twitter analysis
        if trending_topic.twitter_data:
            twitter_metrics = self.twitter_service.get_engagement_metrics(trending_topic.twitter_data)
            summary.engagement_trends['twitter'] = twitter_metrics
            
            # Twitter platform stats
            twitter_stats = PlatformStats(
                platform=PlatformType.TWITTER,
                total_items=len(trending_topic.twitter_data),
                engagement_metrics=twitter_metrics,
                trending_keywords=[tag for tag, _ in twitter_metrics.get('trending_hashtags', [])]
            )
            summary.platform_stats.append(twitter_stats)
        
        # Reddit analysis
        if trending_topic.reddit_data:
            reddit_metrics = self.reddit_service.get_community_metrics(trending_topic.reddit_data)
            summary.engagement_trends['reddit'] = reddit_metrics
            
            # Reddit platform stats
            reddit_stats = PlatformStats(
                platform=PlatformType.REDDIT,
                total_items=len(trending_topic.reddit_data),
                engagement_metrics=reddit_metrics,
                trending_keywords=[kw['keyword'] for kw in self.reddit_service.get_trending_keywords(trending_topic.reddit_data)]
            )
            summary.platform_stats.append(reddit_stats)
        
        return summary
