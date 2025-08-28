import tweepy
from typing import List, Optional, Dict, Any
import re
from datetime import datetime, timedelta
from core.config import settings
from models.trending import TwitterPost

class TwitterService:
    def __init__(self):
        self.api = None
        self.client = None
        self._initialize_api()
    
    def _initialize_api(self):
        """Initialize Twitter API client"""
        try:
            if (settings.TWITTER_API_KEY and settings.TWITTER_API_SECRET and 
                settings.TWITTER_ACCESS_TOKEN and settings.TWITTER_ACCESS_TOKEN_SECRET):
                
                # OAuth 1.0a User Context
                auth = tweepy.OAuthHandler(
                    settings.TWITTER_API_KEY, 
                    settings.TWITTER_API_SECRET
                )
                auth.set_access_token(
                    settings.TWITTER_ACCESS_TOKEN, 
                    settings.TWITTER_ACCESS_TOKEN_SECRET
                )
                self.api = tweepy.API(auth, wait_on_rate_limit=True)
                
            elif settings.TWITTER_BEARER_TOKEN:
                # OAuth 2.0 Bearer Token
                self.client = tweepy.Client(
                    bearer_token=settings.TWITTER_BEARER_TOKEN,
                    wait_on_rate_limit=True
                )
            else:
                print("Warning: No Twitter API credentials provided")
                
        except Exception as e:
            print(f"Error initializing Twitter API: {e}")
    
    def search_trending_posts(self, query: str, max_results: int = 100) -> List[TwitterPost]:
        """Search for trending posts based on query"""
        try:
            if not self.api and not self.client:
                return self._mock_twitter_data(query, max_results)
            
            posts = []
            
            if self.api:
                # Using OAuth 1.0a
                tweets = self.api.search_tweets(
                    q=query,
                    lang='en',
                    count=min(max_results, 100),
                    tweet_mode='extended'
                )
                
                for tweet in tweets:
                    post = self._parse_tweet(tweet)
                    if post:
                        posts.append(post)
                        
            elif self.client:
                # Using OAuth 2.0
                tweets = self.client.search_recent_tweets(
                    query=query,
                    max_results=min(max_results, 100),
                    tweet_fields=['created_at', 'public_metrics', 'entities'],
                    user_fields=['username'],
                    expansions=['author_id']
                )
                
                if tweets.data:
                    users = {user.id: user.username for user in tweets.includes['users']} if 'users' in tweets.includes else {}
                    
                    for tweet in tweets.data:
                        post = self._parse_tweet_v2(tweet, users)
                        if post:
                            posts.append(post)
            
            return posts[:max_results]
            
        except Exception as e:
            print(f"Error searching Twitter posts: {e}")
            return self._mock_twitter_data(query, max_results)
    
    def _parse_tweet(self, tweet) -> Optional[TwitterPost]:
        """Parse tweet from OAuth 1.0a API"""
        try:
            # Extract hashtags
            hashtags = []
            if hasattr(tweet, 'entities') and 'hashtags' in tweet.entities:
                hashtags = [tag['text'] for tag in tweet.entities['hashtags']]
            
            # Extract mentions
            mentions = []
            if hasattr(tweet, 'entities') and 'user_mentions' in tweet.entities:
                mentions = [mention['screen_name'] for mention in tweet.entities['user_mentions']]
            
            return TwitterPost(
                id=str(tweet.id),
                text=tweet.full_text if hasattr(tweet, 'full_text') else tweet.text,
                author_id=str(tweet.user.id),
                author_username=tweet.user.screen_name,
                created_at=tweet.created_at,
                retweet_count=tweet.retweet_count,
                like_count=tweet.favorite_count,
                reply_count=0,  # Not available in OAuth 1.0a
                quote_count=0,   # Not available in OAuth 1.0a
                hashtags=hashtags,
                mentions=mentions
            )
        except Exception as e:
            print(f"Error parsing tweet: {e}")
            return None
    
    def _parse_tweet_v2(self, tweet, users: Dict[str, str]) -> Optional[TwitterPost]:
        """Parse tweet from OAuth 2.0 API"""
        try:
            # Extract hashtags
            hashtags = []
            if tweet.entities and 'hashtags' in tweet.entities:
                hashtags = [tag['tag'] for tag in tweet.entities['hashtags']]
            
            # Extract mentions
            mentions = []
            if tweet.entities and 'mentions' in tweet.entities:
                mentions = [mention['username'] for mention in tweet.entities['mentions']]
            
            return TwitterPost(
                id=str(tweet.id),
                text=tweet.text,
                author_id=str(tweet.author_id),
                author_username=users.get(tweet.author_id, 'unknown'),
                created_at=tweet.created_at,
                retweet_count=tweet.public_metrics['retweet_count'],
                like_count=tweet.public_metrics['like_count'],
                reply_count=tweet.public_metrics['reply_count'],
                quote_count=tweet.public_metrics['quote_count'],
                hashtags=hashtags,
                mentions=mentions
            )
        except Exception as e:
            print(f"Error parsing tweet v2: {e}")
            return None
    
    def _mock_twitter_data(self, query: str, max_results: int) -> List[TwitterPost]:
        """Generate mock Twitter data for testing"""
        posts = []
        base_time = datetime.utcnow()
        
        for i in range(min(max_results, 20)):
            post = TwitterPost(
                id=f"mock_{i}",
                text=f"Mock tweet about {query} #{query.lower()} #python #tech",
                author_id=f"user_{i}",
                author_username=f"user{i}",
                created_at=base_time - timedelta(hours=i),
                retweet_count=i * 10,
                like_count=i * 25,
                reply_count=i * 5,
                quote_count=i * 3,
                hashtags=[query.lower(), 'python', 'tech'],
                mentions=[]
            )
            posts.append(post)
        
        return posts
    
    def get_engagement_metrics(self, posts: List[TwitterPost]) -> Dict[str, Any]:
        """Calculate engagement metrics from posts"""
        if not posts:
            return {}
        
        total_likes = sum(post.like_count for post in posts)
        total_retweets = sum(post.retweet_count for post in posts)
        total_replies = sum(post.reply_count for post in posts)
        total_quotes = sum(post.quote_count for post in posts)
        
        # Calculate engagement rate
        total_engagement = total_likes + total_retweets + total_replies + total_quotes
        avg_engagement_per_post = total_engagement / len(posts)
        
        # Get trending hashtags
        hashtag_counts = {}
        for post in posts:
            for hashtag in post.hashtags:
                hashtag_counts[hashtag] = hashtag_counts.get(hashtag, 0) + 1
        
        trending_hashtags = sorted(
            hashtag_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        return {
            'total_posts': len(posts),
            'total_likes': total_likes,
            'total_retweets': total_retweets,
            'total_replies': total_replies,
            'total_quotes': total_quotes,
            'total_engagement': total_engagement,
            'avg_engagement_per_post': avg_engagement_per_post,
            'trending_hashtags': trending_hashtags,
            'engagement_trend': {
                'likes_ratio': total_likes / total_engagement if total_engagement > 0 else 0,
                'retweets_ratio': total_retweets / total_engagement if total_engagement > 0 else 0,
                'replies_ratio': total_replies / total_engagement if total_engagement > 0 else 0,
                'quotes_ratio': total_quotes / total_engagement if total_engagement > 0 else 0
            }
        }
