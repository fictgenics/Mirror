# Mirror - Technical Deep Dive Guide 🔍

## 🎯 **What This Guide Teaches You**

After reading this guide, you'll understand:
- ✅ **Complete system architecture** and data flow
- ✅ **How trending algorithms work** and how to modify them
- ✅ **How to add new platforms** (YouTube, LinkedIn, etc.)
- ✅ **How to customize scoring** and ranking systems
- ✅ **How to debug issues** and optimize performance
- ✅ **How to extend the API** with new endpoints

---

## 🏗️ **System Architecture Deep Dive**

### **1. High-Level Flow**
```
User Input → Frontend → Backend API → Services → External APIs → Data Processing → Response → Charts
```

### **2. Component Breakdown**

#### **Frontend (React)**
- **Location**: `frontend/src/`
- **Purpose**: User interface and data visualization
- **Key Files**:
  - `App.js` - Main application
  - `pages/` - Different pages (Home, Analysis, Results)
  - `components/` - Reusable UI components

#### **Backend (FastAPI)**
- **Location**: `backend/`
- **Purpose**: API server and business logic
- **Key Files**:
  - `main.py` - Application entry point
  - `api/routes.py` - API endpoints
  - `services/` - Business logic services
  - `models/` - Data structures

#### **Services Layer**
- **Location**: `backend/services/`
- **Purpose**: Platform-specific data collection
- **Key Services**:
  - `github_service.py` - GitHub API integration
  - `twitter_service.py` - Twitter API integration
  - `reddit_service.py` - Reddit API integration
  - `trending_analyzer.py` - Data analysis orchestration

---

## 🔄 **Data Flow Step-by-Step**

### **Step 1: User Input**
```javascript
// User types: "Python machine learning"
const [query, setQuery] = useState('Python machine learning');
```

### **Step 2: Frontend Request**
```javascript
// Frontend sends POST to backend
const response = await axios.post('/api/v1/trending/analyze', {
    query: 'Python machine learning',
    platforms: ['github', 'twitter', 'reddit'],
    max_results_per_platform: 20
});
```

### **Step 3: Backend Processing**
```python
# backend/api/routes.py
@trending_router.post("/analyze")
async def analyze_trending_topic(request: TrendingAnalysisRequest):
    # This calls the trending analyzer
    trending_topic = await trending_analyzer.analyze_trending_topic(request)
```

### **Step 4: Service Execution**
```python
# backend/services/trending_analyzer.py
async def analyze_trending_topic(self, request: TrendingAnalysisRequest):
    # Collect data from all platforms concurrently
    tasks = []
    if PlatformType.GITHUB in request.platforms:
        tasks.append(self._collect_github_data(request.query, request.max_results_per_platform))
```

### **Step 5: External API Calls**
```python
# backend/services/github_service.py
def search_trending_repos(self, query: str, max_results: int = 20):
    # Search GitHub API
    search_query = f"{query} created:>2024-01-01"
    repos = self.github.search_repositories(search_query, sort='stars', order='desc')
```

### **Step 6: Data Processing & Scoring**
```python
# Calculate trending scores
trending_topic.overall_score = self._calculate_overall_score(trending_topic)
```

### **Step 7: Response & Display**
```javascript
// Frontend displays results
const renderOverviewTab = () => (
    <div className="text-4xl font-bold text-primary-600">
        {analysisData.overall_score ? Math.round(analysisData.overall_score) : 'N/A'}
    </div>
);
```

---

## 🧮 **Trending Algorithm Explained**

### **Overall Score Formula:**
```
Overall Score = GitHub Score = (avg_stars × 0.5) + (avg_forks × 0.3) + (avg_contributors × 0.2)
```

### **GitHub Score (40% weight):**
```python
def _calculate_github_score(self, repos: List) -> float:
    total_stars = sum(repo.stargazers_count for repo in repos)
    total_forks = sum(repo.forks_count for repo in repos)
    total_contributors = sum(repo.contributors_count or 0 for repo in repos)
    
    avg_stars = total_stars / len(repos)
    avg_forks = total_forks / len(repos)
    avg_contributors = total_contributors / len(repos)
    
    # Weighted scoring
    score = (avg_stars * 0.5) + (avg_forks * 0.3) + (avg_contributors * 0.2)
    
    # Normalize to 0-100 scale
    return min(score / 1000, 100.0)
```

**What This Means:**
- **Stars (50%)**: Repository popularity and viral growth
- **Forks (30%)**: Repository adoption and usage
- **Contributors (20%)**: Community involvement and activity

### **Twitter Score (35% weight):**
```python
def _calculate_twitter_score(self, posts: List) -> float:
    total_likes = sum(post.like_count for post in posts)
    total_retweets = sum(post.retweet_count for post in posts)
    total_replies = sum(post.reply_count for post in posts)
    
    total_engagement = total_likes + total_retweets + total_replies
    avg_engagement = total_engagement / len(posts)
    
    return min(avg_engagement / 100, 100.0)
```

### **Reddit Score (25% weight):**
```python
def _calculate_reddit_score(self, posts: List) -> float:
    total_score = sum(post.score for post in posts)
    total_comments = sum(post.num_comments for post in posts)
    
    avg_score = total_score / len(posts)
    avg_comments = total_comments / len(posts)
    
    score = (avg_score * 0.7) + (avg_comments * 0.3)
    
    return min(score / 100, 100.0)
```

---

## 🔧 **How to Make Changes**

### **1. Adding New Platforms**

#### **Step 1: Create Platform Service**
```python
# backend/services/youtube_service.py
class YouTubeService:
    def __init__(self):
        self.api_key = settings.YOUTUBE_API_KEY
    
    def search_trending_videos(self, query: str, max_results: int) -> List[YouTubeVideo]:
        # Implementation here
        pass
```

#### **Step 2: Add Platform Type**
```python
# backend/models/trending.py
class PlatformType(str, Enum):
    GITHUB = "github"
    TWITTER = "twitter"
    REDDIT = "reddit"
    YOUTUBE = "youtube"  # Add this
```

#### **Step 3: Create Data Model**
```python
class YouTubeVideo(BaseModel):
    id: str
    title: str
    view_count: int
    like_count: int
    comment_count: int
    published_at: datetime
```

#### **Step 4: Integrate with Analyzer**
```python
# backend/services/trending_analyzer.py
async def _collect_youtube_data(self, query: str, max_results: int) -> List:
    return await self.youtube_service.search_trending_videos(query, max_results)

def _calculate_youtube_score(self, videos: List) -> float:
    # Implement scoring logic
    pass
```

### **2. Modifying Trending Algorithm**

#### **Change Platform Weights:**
```python
# backend/services/trending_analyzer.py
def _calculate_overall_score(self, trending_topic: TrendingTopic) -> float:
    # Change these weights
    github_weight = 0.5      # Was 0.4
    twitter_weight = 0.3     # Was 0.35
    reddit_weight = 0.2      # Was 0.25
```

#### **Modify GitHub Scoring:**
```python
# backend/services/github_service.py
def _calculate_github_score(self, repos: List) -> float:
    # Change metric weights
    star_weight = 0.6        # Was 0.5
    fork_weight = 0.25       # Was 0.3
    contributor_weight = 0.15 # Was 0.2
    
    score = (avg_stars * star_weight) + (avg_forks * fork_weight) + (avg_contributors * contributor_weight)
```

#### **Add New Metrics:**
```python
def _calculate_github_score(self, repos: List) -> float:
    # Add new metrics
    total_issues = sum(repo.open_issues_count for repo in repos)
    avg_issues = total_issues / len(repos)
    
    # Include in scoring
    score = (avg_stars * 0.4) + (avg_forks * 0.3) + (avg_contributors * 0.2) + (avg_issues * 0.1)
```

### **3. Adding New API Endpoints**

#### **Create New Route:**
```python
# backend/api/routes.py
@trending_router.get("/trending-history")
async def get_trending_history():
    """Get historical trending data"""
    return {"message": "Historical data endpoint"}
```

#### **Frontend Integration:**
```javascript
// frontend/src/pages/ResultsPage.js
const fetchTrendingHistory = async () => {
    const response = await axios.get('/api/v1/trending/trending-history');
    // Handle response
};
```

### **4. Adding New Visualizations**

#### **Create Chart Component:**
```javascript
// frontend/src/components/NewChart.js
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const NewChart = ({ data }) => {
    return (
        <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
                <LineChart data={data}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Line type="monotone" dataKey="value" stroke="#8884d8" />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
};
```

---

## 🚨 **Troubleshooting Guide**

### **Common Issues:**

#### **1. Backend Won't Start**
```bash
# Install dependencies
pip install -r requirements.txt

# Check if port is free
lsof -i :8000
kill -9 <PID>
```

#### **2. Frontend Won't Start**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm start
```

#### **3. API Calls Failing**
```bash
# Check API keys in .env file
cat .env

# Test API connectivity
curl -H "Authorization: token YOUR_GITHUB_TOKEN" https://api.github.com/user
```

#### **4. Data Not Loading**
```python
# Add logging in services
print(f"API Response: {response}")
print(f"Query: {query}")
```

### **Debugging Techniques:**

#### **Backend Logging:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def search_trending_repos(self, query: str, max_results: int = 20):
    logger.debug(f"Searching GitHub for: {query}")
```

#### **Frontend Console:**
```javascript
console.log('API Response:', response.data);
console.log('Analysis Data:', analysisData);
```

#### **API Testing:**
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test analysis endpoint
curl -X POST "http://localhost:8000/api/v1/trending/analyze" \
     -H "Content-Type: application/json" \
     -d '{"query": "test", "platforms": ["github"], "max_results_per_platform": 5}'
```

---

## 🎯 **What You Can Do Now**

With this knowledge, you can:

1. **Add new data sources** (YouTube, LinkedIn, Stack Overflow)
2. **Customize trending algorithms** and scoring weights
3. **Create new API endpoints** for additional features
4. **Add new visualizations** and chart types
5. **Modify data models** to include new fields
6. **Debug issues** and optimize performance
7. **Extend the system** with new capabilities

## 🚀 **Next Steps**

1. **Try modifying the GitHub scoring weights** in `github_service.py`
2. **Add a new API endpoint** for trending history
3. **Create a new chart component** for different data visualization
4. **Experiment with different platform weights** in the trending algorithm

The Mirror project is designed to be **modular and extensible**, so you can easily add new features while maintaining the existing architecture.

**Happy coding! 🎉✨**
