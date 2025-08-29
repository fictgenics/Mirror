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
