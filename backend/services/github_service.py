import github3
from typing import List, Optional, Dict, Any
import requests
from datetime import datetime, timedelta
import time
from core.config import settings
from models.trending import GitHubRepo

class GitHubService:
    def __init__(self):
        self.token = settings.GITHUB_TOKEN
        self.github = None
        if self.token:
            self.github = github3.login(token=self.token)
    
    def search_trending_repos(self, query: str, max_results: int = 20) -> List[GitHubRepo]:
        """Search for trending repositories based on query"""
        try:
            if not self.github:
                # Fallback to unauthenticated requests
                return self._search_repos_unauthenticated(query, max_results)
            
            # Search repositories
            search_query = f"{query} created:>2024-01-01"
            repos = self.github.search_repositories(search_query, sort='stars', order='desc')
            
            repo_list = []
            for repo in repos:
                if len(repo_list) >= max_results:
                    break
                
                try:
                    # Get additional repository information
                    repo_data = self._enrich_repo_data(repo)
                    repo_list.append(repo_data)
                    time.sleep(0.1)  # Rate limiting
                except Exception as e:
                    print(f"Error enriching repo {repo.full_name}: {e}")
                    continue
            
            return repo_list
            
        except Exception as e:
            print(f"Error searching GitHub repos: {e}")
            return []
    
    def _search_repos_unauthenticated(self, query: str, max_results: int) -> List[GitHubRepo]:
        """Search repositories without authentication (limited)"""
        try:
            url = "https://api.github.com/search/repositories"
            params = {
                'q': f"{query} created:>2024-01-01",
                'sort': 'stars',
                'order': 'desc',
                'per_page': min(max_results, 30)  # GitHub API limit for unauthenticated
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            repo_list = []
            
            for repo_data in data.get('items', []):
                repo = GitHubRepo(
                    name=repo_data['name'],
                    full_name=repo_data['full_name'],
                    description=repo_data.get('description'),
                    html_url=repo_data['html_url'],
                    stargazers_count=repo_data['stargazers_count'],
                    forks_count=repo_data['forks_count'],
                    language=repo_data.get('language'),
                    topics=repo_data.get('topics', []),
                    created_at=datetime.fromisoformat(repo_data['created_at'].replace('Z', '+00:00')),
                    updated_at=datetime.fromisoformat(repo_data['updated_at'].replace('Z', '+00:00')),
                    open_issues_count=repo_data['open_issues_count'],
                    contributors_count=None,
                    commits_count=None,
                    tech_stack=[]
                )
                repo_list.append(repo)
            
            return repo_list
            
        except Exception as e:
            print(f"Error in unauthenticated GitHub search: {e}")
            return []
    
    def _enrich_repo_data(self, repo) -> GitHubRepo:
        """Enrich repository data with additional information"""
        try:
            # Get topics
            topics = []
            try:
                topics = [topic.name for topic in repo.topics()]
            except:
                pass
            
            # Get contributors count
            contributors_count = None
            try:
                contributors = repo.contributors()
                contributors_count = len(list(contributors))
            except:
                pass
            
            # Get commits count (approximate)
            commits_count = None
            try:
                commits = repo.commits()
                commits_count = len(list(commits))
            except:
                pass
            
            # Determine tech stack from language and topics
            tech_stack = []
            if repo.language:
                tech_stack.append(repo.language)
            tech_stack.extend(topics)
            
            return GitHubRepo(
                name=repo.name,
                full_name=repo.full_name,
                description=repo.description,
                html_url=repo.html_url,
                stargazers_count=repo.stargazers_count,
                forks_count=repo.forks_count,
                language=repo.language,
                topics=topics,
                created_at=repo.created_at,
                updated_at=repo.updated_at,
                open_issues_count=repo.open_issues_count,
                contributors_count=contributors_count,
                commits_count=commits_count,
                tech_stack=tech_stack
            )
            
        except Exception as e:
            print(f"Error enriching repo data: {e}")
            raise
    
    def get_trending_languages(self, repos: List[GitHubRepo]) -> List[Dict[str, Any]]:
        """Analyze trending programming languages from repositories"""
        language_stats = {}
        
        for repo in repos:
            if repo.language:
                if repo.language not in language_stats:
                    language_stats[repo.language] = {
                        'count': 0,
                        'total_stars': 0,
                        'total_forks': 0
                    }
                
                language_stats[repo.language]['count'] += 1
                language_stats[repo.language]['total_stars'] += repo.stargazers_count
                language_stats[repo.language]['total_forks'] += repo.forks_count
        
        # Sort by count and then by total stars
        sorted_languages = sorted(
            language_stats.items(),
            key=lambda x: (x[1]['count'], x[1]['total_stars']),
            reverse=True
        )
        
        return [
            {
                'language': lang,
                'count': stats['count'],
                'total_stars': stats['total_stars'],
                'total_forks': stats['total_forks'],
                'avg_stars': stats['total_stars'] / stats['count']
            }
            for lang, stats in sorted_languages[:10]  # Top 10 languages
        ]
    
    def get_top_contributors(self, repos: List[GitHubRepo]) -> List[Dict[str, Any]]:
        """Get top contributors based on repository activity"""
        contributor_stats = {}
        
        for repo in repos:
            if repo.contributors_count:
                # Simple scoring based on repository popularity
                score = repo.stargazers_count + repo.forks_count * 2
                
                if repo.full_name not in contributor_stats:
                    contributor_stats[repo.full_name] = {
                        'repo_name': repo.full_name,
                        'score': score,
                        'stars': repo.stargazers_count,
                        'forks': repo.forks_count,
                        'language': repo.language
                    }
        
        # Sort by score
        sorted_contributors = sorted(
            contributor_stats.values(),
            key=lambda x: x['score'],
            reverse=True
        )
        
        return sorted_contributors[:10]  # Top 10 contributors
