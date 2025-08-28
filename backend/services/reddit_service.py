import praw
from typing import List, Optional, Dict, Any
import re
from datetime import datetime, timedelta
from core.config import settings
from models.trending import RedditPost

class RedditService:
    def __init__(self):
        self.reddit = None
        self._initialize_api()
    
    def _initialize_api(self):
        """Initialize Reddit API client"""
        try:
            if (settings.REDDIT_CLIENT_ID and 
                settings.REDDIT_CLIENT_SECRET and 
                settings.REDDIT_USER_AGENT):
                
                self.reddit = praw.Reddit(
                    client_id=settings.REDDIT_CLIENT_ID,
                    client_secret=settings.REDDIT_CLIENT_SECRET,
                    user_agent=settings.REDDIT_USER_AGENT
                )
            else:
                print("Warning: No Reddit API credentials provided")
                
        except Exception as e:
            print(f"Error initializing Reddit API: {e}")
    
    def search_trending_posts(self, query: str, max_results: int = 50) -> List[RedditPost]:
        """Search for trending posts based on query"""
        try:
            if not self.reddit:
                return self._mock_reddit_data(query, max_results)
            
            posts = []
            
            # Search across multiple programming/tech subreddits
            subreddits = [
                'programming', 'Python', 'javascript', 'webdev', 
                'MachineLearning', 'datascience', 'technology',
                'coding', 'learnprogramming', 'opensource'
            ]
            
            for subreddit_name in subreddits:
                if len(posts) >= max_results:
                    break
                
                try:
                    subreddit = self.reddit.subreddit(subreddit_name)
                    
                    # Search for posts
                    search_results = subreddit.search(
                        query, 
                        sort='hot', 
                        time_filter='week',
                        limit=min(20, max_results - len(posts))
                    )
                    
                    for submission in search_results:
                        if len(posts) >= max_results:
                            break
                        
                        try:
                            post = self._parse_submission(submission)
                            if post:
                                posts.append(post)
                        except Exception as e:
                            print(f"Error parsing submission: {e}")
                            continue
                            
                except Exception as e:
                    print(f"Error searching subreddit {subreddit_name}: {e}")
                    continue
            
            return posts[:max_results]
            
        except Exception as e:
            print(f"Error searching Reddit posts: {e}")
            return self._mock_reddit_data(query, max_results)
    
    def _parse_submission(self, submission) -> Optional[RedditPost]:
        """Parse Reddit submission into RedditPost model"""
        try:
            # Extract domain from URL
            domain = submission.domain if hasattr(submission, 'domain') else 'reddit.com'
            
            # Determine if it's a self post
            is_self = submission.is_self if hasattr(submission, 'is_self') else False
            
            # Get selftext (content for self posts)
            selftext = submission.selftext if hasattr(submission, 'selftext') else ""
            
            # Convert timestamp to datetime
            created_time = datetime.fromtimestamp(submission.created_utc)
            
            return RedditPost(
                id=submission.id,
                title=submission.title,
                selftext=selftext,
                author=str(submission.author) if submission.author else 'deleted',
                subreddit=submission.subreddit.display_name,
                score=submission.score,
                upvote_ratio=getattr(submission, 'upvote_ratio', 0.0),
                num_comments=submission.num_comments,
                created_utc=created_time,
                url=submission.url,
                is_self=is_self,
                domain=domain
            )
            
        except Exception as e:
            print(f"Error parsing submission: {e}")
            return None
    
    def _mock_reddit_data(self, query: str, max_results: int) -> List[RedditPost]:
        """Generate mock Reddit data for testing"""
        posts = []
        base_time = datetime.utcnow()
        subreddits = ['programming', 'Python', 'javascript', 'webdev', 'technology']
        
        for i in range(min(max_results, 20)):
            subreddit = subreddits[i % len(subreddits)]
            post = RedditPost(
                id=f"mock_{i}",
                title=f"Mock Reddit post about {query} in {subreddit}",
                selftext=f"This is a mock post discussing {query} and its applications in {subreddit}.",
                author=f"user{i}",
                subreddit=subreddit,
                score=i * 50 + 100,
                upvote_ratio=0.85 + (i * 0.01),
                num_comments=i * 10 + 5,
                created_utc=base_time - timedelta(hours=i),
                url=f"https://reddit.com/r/{subreddit}/comments/mock_{i}",
                is_self=True,
                domain="reddit.com"
            )
            posts.append(post)
        
        return posts
    
    def get_community_metrics(self, posts: List[RedditPost]) -> Dict[str, Any]:
        """Calculate community engagement metrics from posts"""
        if not posts:
            return {}
        
        # Subreddit statistics
        subreddit_stats = {}
        for post in posts:
            subreddit = post.subreddit
            if subreddit not in subreddit_stats:
                subreddit_stats[subreddit] = {
                    'count': 0,
                    'total_score': 0,
                    'total_comments': 0,
                    'avg_upvote_ratio': 0.0
                }
            
            subreddit_stats[subreddit]['count'] += 1
            subreddit_stats[subreddit]['total_score'] += post.score
            subreddit_stats[subreddit]['total_comments'] += post.num_comments
            subreddit_stats[subreddit]['avg_upvote_ratio'] += post.upvote_ratio
        
        # Calculate averages
        for subreddit in subreddit_stats:
            count = subreddit_stats[subreddit]['count']
            subreddit_stats[subreddit]['avg_score'] = subreddit_stats[subreddit]['total_score'] / count
            subreddit_stats[subreddit]['avg_comments'] = subreddit_stats[subreddit]['total_comments'] / count
            subreddit_stats[subreddit]['avg_upvote_ratio'] = subreddit_stats[subreddit]['avg_upvote_ratio'] / count
        
        # Overall metrics
        total_score = sum(post.score for post in posts)
        total_comments = sum(post.num_comments for post in posts)
        avg_upvote_ratio = sum(post.upvote_ratio for post in posts) / len(posts)
        
        # Top performing posts
        top_posts = sorted(posts, key=lambda x: x.score, reverse=True)[:5]
        
        # Most active subreddits
        most_active_subreddits = sorted(
            subreddit_stats.items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )[:5]
        
        return {
            'total_posts': len(posts),
            'total_score': total_score,
            'total_comments': total_comments,
            'avg_score_per_post': total_score / len(posts),
            'avg_comments_per_post': total_comments / len(posts),
            'avg_upvote_ratio': avg_upvote_ratio,
            'subreddit_stats': subreddit_stats,
            'top_posts': [
                {
                    'title': post.title,
                    'score': post.score,
                    'comments': post.num_comments,
                    'subreddit': post.subreddit
                }
                for post in top_posts
            ],
            'most_active_subreddits': most_active_subreddits,
            'engagement_trend': {
                'high_engagement_posts': len([p for p in posts if p.score > 100]),
                'medium_engagement_posts': len([p for p in posts if 50 <= p.score <= 100]),
                'low_engagement_posts': len([p for p in posts if p.score < 50])
            }
        }
    
    def get_trending_keywords(self, posts: List[RedditPost]) -> List[Dict[str, Any]]:
        """Extract trending keywords from post titles and content"""
        keyword_counts = {}
        
        for post in posts:
            # Combine title and selftext
            text = f"{post.title} {post.selftext}".lower()
            
            # Extract words (simple approach)
            words = re.findall(r'\b\w+\b', text)
            
            # Filter out common words and short words
            common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their'}
            
            for word in words:
                if len(word) > 3 and word not in common_words and word.isalpha():
                    keyword_counts[word] = keyword_counts.get(word, 0) + 1
        
        # Sort by frequency
        trending_keywords = sorted(
            keyword_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:15]  # Top 15 keywords
        
        return [
            {
                'keyword': keyword,
                'count': count,
                'percentage': (count / len(posts)) * 100
            }
            for keyword, count in trending_keywords
        ]
