from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import List

from models.trending import (
    TrendingAnalysisRequest, TrendingAnalysisResponse, 
    PlatformType, AnalysisSummary
)
from services.trending_analyzer import TrendingAnalyzer

# Create router
trending_router = APIRouter(prefix="/trending", tags=["trending"])

# Initialize services
trending_analyzer = TrendingAnalyzer()

@trending_router.post("/analyze", response_model=TrendingAnalysisResponse)
async def analyze_trending_topic(request: TrendingAnalysisRequest):
    """
    Analyze trending topics across multiple platforms
    """
    try:
        # Validate request
        if not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        if not request.platforms:
            raise HTTPException(status_code=400, detail="At least one platform must be selected")
        
        # Perform analysis
        trending_topic = await trending_analyzer.analyze_trending_topic(request)
        
        # Generate summary
        summary = trending_analyzer.generate_analysis_summary(trending_topic)
        
        return TrendingAnalysisResponse(
            success=True,
            message=f"Successfully analyzed trending topic: {request.query}",
            data=trending_topic
        )
        
    except Exception as e:
        return TrendingAnalysisResponse(
            success=False,
            message="Error analyzing trending topic",
            error=str(e)
        )

@trending_router.get("/platforms")
async def get_available_platforms():
    """
    Get list of available platforms for analysis
    """
    return {
        "platforms": [
            {
                "id": PlatformType.GITHUB,
                "name": "GitHub",
                "description": "Analyze trending repositories, languages, and contributors",
                "capabilities": ["Repository analysis", "Language trends", "Contributor insights"]
            }
        ]
    }

@trending_router.get("/health")
async def health_check():
    """
    Health check for trending analysis service
    """
    return {
        "status": "healthy",
        "service": "Trending Analysis",
        "available_platforms": len(PlatformType),
        "timestamp": "2024-01-01T00:00:00Z"
    }

@trending_router.get("/example-queries")
async def get_example_queries():
    """
    Get example queries for trending analysis
    """
    return {
        "example_queries": [
            {
                "query": "Python machine learning",
                "description": "Analyze trending topics in Python ML ecosystem",
                "expected_insights": ["Popular ML libraries", "GitHub repositories", "Community discussions"]
            },
            {
                "query": "JavaScript frameworks",
                "description": "Explore trending JavaScript frameworks and tools",
                "expected_insights": ["Framework popularity", "GitHub stars", "Developer sentiment"]
            },
            {
                "query": "Data science tools",
                "description": "Discover trending data science tools and platforms",
                "expected_insights": ["Tool adoption", "Community engagement", "GitHub activity"]
            },
            {
                "query": "Web development trends",
                "description": "Analyze current web development trends",
                "expected_insights": ["Technology adoption", "Community discussions", "Repository activity"]
            },
            {
                "query": "Open source projects",
                "description": "Explore trending open source projects",
                "expected_insights": ["Project popularity", "Contributor activity", "Community engagement"]
            }
        ]
    }

@trending_router.post("/quick-analysis")
async def quick_analysis(query: str, platforms: List[PlatformType] = None):
    """
    Quick analysis with minimal configuration
    """
    if not platforms:
        platforms = [PlatformType.GITHUB]
    
    request = TrendingAnalysisRequest(
        query=query,
        platforms=platforms,
        max_results_per_platform=15
    )
    
    try:
        trending_topic = await trending_analyzer.analyze_trending_topic(request)
        summary = trending_analyzer.generate_analysis_summary(trending_topic)
        
        return {
            "success": True,
            "query": query,
            "overall_score": trending_topic.overall_score,
                            "summary": {
                    "total_repos": summary.total_repos,
                    "top_languages": summary.top_languages[:5],
                    "platform_stats": [
                        {
                            "platform": stat.platform,
                            "total_items": stat.total_items,
                            "trending_keywords": stat.trending_keywords[:5]
                        }
                        for stat in summary.platform_stats
                    ]
                }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@trending_router.post("/nlp-search")
async def nlp_based_search(natural_query: str, max_results: int = 20):
    """
    Search repositories using natural language processing
    
    Examples:
    - "repos with more than 100 stars where mcp server is used to connect notion"
    - "python projects with at least 50 forks created since 2023"
    - "javascript libraries with typescript support and more than 200 stars"
    """
    try:
        nlp_results = await trending_analyzer.analyze_trending_with_nlp(natural_query, max_results)
        
        if "error" in nlp_results:
            return {
                "success": False,
                "error": nlp_results["error"]
            }
        
        return {
            "success": True,
            "natural_query": natural_query,
            "parsed_query": nlp_results["query_analysis"]["original_query"],
            "github_query": nlp_results["search_query"],
            "parsed_filters": nlp_results["parsed_filters"],
            "total_repos": nlp_results["trending_topic"].overall_score,
            "repositories": [
                {
                    "name": repo.name,
                    "full_name": repo.full_name,
                    "description": repo.description,
                    "html_url": repo.html_url,
                    "stargazers_count": repo.stargazers_count,
                    "forks_count": repo.forks_count,
                    "language": repo.language,
                    "topics": repo.topics,
                    "created_at": repo.created_at.isoformat(),
                    "updated_at": repo.updated_at.isoformat(),
                    "open_issues_count": repo.open_issues_count,
                    "contributors_count": repo.contributors_count,
                    "commits_count": repo.commits_count,
                    "tech_stack": repo.tech_stack
                }
                for repo in nlp_results["trending_topic"].github_data
            ],
            "summary": {
                "total_repos": nlp_results["summary"].total_repos,
                "top_languages": nlp_results["summary"].top_languages[:5],
                "overall_score": nlp_results["trending_topic"].overall_score
            },
            "search_suggestions": nlp_results["suggestions"]
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@trending_router.get("/nlp-examples")
async def get_nlp_examples():
    """
    Get examples of natural language queries
    """
    return {
        "nlp_examples": [
            {
                "query": "repos with more than 100 stars where mcp server is used to connect notion",
                "description": "Find popular MCP server implementations for Notion integration",
                "parses_to": "mcp server + topic:notion + stars:>=100"
            },
            {
                "query": "python projects with at least 50 forks created since 2023",
                "description": "Find active Python projects with community engagement",
                "parses_to": "python + forks:>=50 + created:>=2023-01-01"
            },
            {
                "query": "javascript libraries with typescript support and more than 200 stars",
                "description": "Find popular JS libraries with TypeScript support",
                "parses_to": "javascript + topic:typescript + stars:>=200"
            },
            {
                "query": "machine learning tools in python with more than 1000 stars",
                "description": "Find highly popular Python ML tools",
                "parses_to": "machine learning + language:python + stars:>=1000"
            },
            {
                "query": "web frameworks with react support and at least 500 forks",
                "description": "Find popular web frameworks supporting React",
                "parses_to": "web frameworks + topic:react + forks:>=500"
            }
        ],
        "supported_patterns": [
            "more than X stars/forks/contributors",
            "at least X stars/forks/contributors", 
            "in [language]",
            "created since [year]",
            "with [topic]",
            "using [technology]",
            "has issues/wiki",
            "archived/not archived",
            "forked/not forked"
        ]
    }
