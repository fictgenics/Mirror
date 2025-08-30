import github3
from typing import List, Optional, Dict, Any
import requests
from datetime import datetime
import time
from core.config import settings
from services.nlp_parser import NLPQueryParser, ParsedQuery
from models.trending import GitHubRepo
from services.nlp_services import SemanticSearch


class GitHubService:
    def __init__(self):
        self.token = settings.GITHUB_TOKEN
        self.github = None
        self.nlp_services = SemanticSearch()   # ✅ initialize NLP service
        if self.token:
            self.github = github3.login(token=self.token)

    def search_trending_repos(self, query: str, max_results: int = 20) -> List[GitHubRepo]:
        """Search for trending repositories based on query"""
        try:
            if not self.github:
                # Fallback to unauthenticated requests
                return self._search_repos_unauthenticated(query, max_results)

            # Search repositories
            search_query = f"{query}"
            repos = self.github.search_repositories(search_query, sort='stars', order='desc')

            repo_list = []
            for repo in repos:
                if len(repo_list) >= max_results:
                    break

                try:
                    # Get additional repository information
                    repo_data = self._enrich_repo_data(repo)
                    repo_with_metrics = self.compute_repo_metrics(repo_data)
                    repo_list.append(repo_with_metrics)
                    time.sleep(0.1)  # Rate limiting
                except Exception as e:
                    print(f"Error enriching repo {repo.full_name}: {e}")
                    continue

            return repo_list

        except Exception as e:
            print(f"Error searching GitHub repos: {e}")
            return []

    async def _search_repos_unauthenticated(self, query: str, max_results: int) -> List[GitHubRepo]:
        """Search repositories without authentication (limited)"""
        try:
            url = "https://api.github.com/search/repositories"
            params = {
                'q': f"{query}",
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
                repo_with_metrics = self.compute_repo_metrics(repo)
                repo_list.append(repo_with_metrics)

            return repo_list

        except Exception as e:
            print(f"Error in unauthenticated GitHub search: {e}")
            return []

    def compute_repo_metrics(self, repo: GitHubRepo) -> GitHubRepo:
        """Enhance repo with extra metrics like stars/day, health score"""
        try:
            # Stars per day
            days_old = max((datetime.utcnow() - repo.created_at).days, 1)
            repo.stars_per_day = repo.stargazers_count / days_old

            # Stars per contributor
            if repo.contributors_count:
                repo.stars_per_contributor = repo.stargazers_count / repo.contributors_count

            # Health score (example formula)
            activity_score = 1 / max((datetime.utcnow() - repo.updated_at).days, 1)
            issue_penalty = repo.open_issues_count / max(repo.stargazers_count + repo.forks_count, 1)

            repo.health_score = (
                repo.stargazers_count * 0.6 +
                repo.forks_count * 0.3 +
                activity_score * 100 -
                issue_penalty * 50
            )

        except Exception as e:
            print(f"Error computing metrics for {repo.full_name}: {e}")

        return repo

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

    def search_with_nlp(self, natural_query: str, max_results: int = 20) -> Dict[str, Any]:
        """Search repositories using natural language processing"""
        try:
            # Initialize NLP parser
            nlp_parser = NLPQueryParser()
            
            # Parse the natural language query
            parsed_query = nlp_parser.parse_query(natural_query)
            
            # Build GitHub search query
            github_query = nlp_parser.build_github_query(parsed_query)
            
            # Get query explanation
            explanation = nlp_parser.get_query_explanation(parsed_query)
            
            # Perform the search
            repos = self.search_trending_repos(github_query, max_results)
            
            return {
                "repositories": repos,
                "query_analysis": explanation,
                "total_found": len(repos),
                "search_query": github_query,
                "parsed_filters": explanation["parsed_filters"]
            }
            
        except Exception as e:
            print(f"Error in NLP search: {e}")
            return {
                "repositories": [],
                "query_analysis": {"error": str(e)},
                "total_found": 0,
                "search_query": natural_query,
                "parsed_filters": {}
            }

    def get_semantic_search_suggestions(self, query: str) -> List[str]:
        """Get semantic search suggestions based on the query"""
        suggestions = []
        
        # Common patterns for different types of searches
        if "mcp" in query.lower() or "model context protocol" in query.lower():
            suggestions.extend([
                "mcp server implementation",
                "model context protocol tools",
                "mcp client libraries",
                "mcp integration examples"
            ])
        
        if "notion" in query.lower():
            suggestions.extend([
                "notion api integration",
                "notion database sync",
                "notion automation tools",
                "notion webhook handlers"
            ])
        
        if "100" in query and "stars" in query.lower():
            suggestions.extend([
                "highly starred repositories",
                "popular open source projects",
                "trending repositories",
                "well-maintained projects"
            ])
        
        # Add generic suggestions
        suggestions.extend([
            f"repositories about {query}",
            f"tools for {query}",
            f"libraries related to {query}",
            f"frameworks for {query}"
        ])
        
        return list(set(suggestions))[:5]  # Return unique suggestions, max 5
