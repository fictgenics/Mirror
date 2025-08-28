# Mirror - Technical Deep Dive Documentation 🔍

## 📚 **Table of Contents**
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Data Flow Deep Dive](#data-flow-deep-dive)
4. [API Design & Endpoints](#api-design--endpoints)
5. [Database Models & Data Structures](#database-models--data-structures)
6. [Service Layer Architecture](#service-layer-architecture)
7. [Frontend Architecture](#frontend-architecture)
8. [Trending Algorithm Explained](#trending-algorithm-explained)
9. [How to Make Changes](#how-to-make-changes)
10. [Troubleshooting Guide](#troubleshooting-guide)

---

## 🎯 **Project Overview**

**Mirror** is a **trending topics analyzer** that collects data from multiple platforms (GitHub, Twitter/X, Reddit) and provides insights through data visualization.

### **What It Does:**
- Searches trending topics across platforms
- Analyzes engagement metrics and popularity
- Calculates trending scores using algorithms
- Presents data through interactive charts
- Provides comprehensive insights and analysis

### **Key Technologies:**
- **Backend**: FastAPI (Python)
- **Frontend**: React + TypeScript
- **Data Visualization**: Recharts, Chart.js
- **Styling**: Tailwind CSS
- **APIs**: GitHub, Twitter, Reddit

---

## 🏗️ **System Architecture**

### **High-Level Architecture:**
```
┌─────────────────┐    HTTP Requests    ┌─────────────────┐
│   Frontend      │ ──────────────────► │    Backend      │
│   (React)       │                     │   (FastAPI)     │
│   Port 3000     │                     │   Port 8000     │
└─────────────────┘                     └─────────────────┘
                                                │
                                                ▼
                                    ┌─────────────────┐
                                    │   Services      │
                                    │   Layer         │
                                    └─────────────────┘
                                                │
                                                ▼
                                    ┌─────────────────┐
                                    │   External      │
                                    │   APIs          │
                                    └─────────────────┘
```

### **Component Breakdown:**

#### **1. Frontend (React)**
- **Location**: `frontend/src/`
- **Purpose**: User interface and data visualization
- **Key Files**:
  - `App.js` - Main application component
  - `pages/` - Different application pages
  - `components/` - Reusable UI components
  - `styles/` - CSS and styling

#### **2. Backend (FastAPI)**
- **Location**: `backend/`
- **Purpose**: API server and business logic
- **Key Files**:
  - `main.py` - Application entry point
  - `api/routes.py` - API endpoints
  - `services/` - Business logic services
  - `models/` - Data structures

#### **3. Services Layer**
- **Location**: `backend/services/`
- **Purpose**: Platform-specific data collection
- **Key Services**:
  - `github_service.py` - GitHub API integration
  - `twitter_service.py` - Twitter API integration
  - `reddit_service.py` - Reddit API integration
  - `trending_analyzer.py` - Data analysis orchestration

---

## 🔄 **Data Flow Deep Dive**

### **Complete Data Flow:**
```
1. User Input → 2. Frontend → 3. Backend API → 4. Services → 5. External APIs → 6. Data Processing → 7. Response → 8. Frontend Display
```

### **Step-by-Step Breakdown:**

#### **Step 1: User Input**
```javascript
// frontend/src/pages/AnalysisPage.js
const [query, setQuery] = useState('');
const [selectedPlatforms, setSelectedPlatforms] = useState(['github', 'twitter', 'reddit']);
```

#### **Step 2: Frontend Request**
```javascript
const response = await axios.post('/api/v1/trending/analyze', {
    query: query.trim(),
    platforms: selectedPlatforms,
    max_results_per_platform: 20
});
```

#### **Step 3: Backend API Processing**
```python
# backend/api/routes.py
@trending_router.post("/analyze")
async def analyze_trending_topic(request: TrendingAnalysisRequest):
    trending_topic = await trending_analyzer.analyze_trending_topic(request)
```

#### **Step 4: Service Layer Execution**
```python
# backend/services/trending_analyzer.py
async def analyze_trending_topic(self, request: TrendingAnalysisRequest):
    # Collect data from all platforms concurrently
    tasks = []
    if PlatformType.GITHUB in request.platforms:
        tasks.append(self._collect_github_data(request.query, request.max_results_per_platform))
```

#### **Step 5: External API Calls**
```python
# backend/services/github_service.py
def search_trending_repos(self, query: str, max_results: int = 20):
    search_query = f"{query} created:>2024-01-01"
    repos = self.github.search_repositories(search_query, sort='stars', order='desc')
```

#### **Step 6: Data Processing & Scoring**
```python
# Calculate trending scores
trending_topic.overall_score = self._calculate_overall_score(trending_topic)
```

#### **Step 7: Response Generation**
```python
return TrendingAnalysisResponse(
    success=True,
    message=f"Successfully analyzed trending topic: {request.query}",
    data=trending_topic
)
```

#### **Step 8: Frontend Display**
```javascript
// frontend/src/pages/ResultsPage.js
const renderOverviewTab = () => (
    <div className="text-4xl font-bold text-primary-600 mb-2">
        {analysisData.overall_score ? Math.round(analysisData.overall_score) : 'N/A'}
    </div>
);
```

---

## 🌐 **API Design & Endpoints**

### **API Base URL**: `http://localhost:8000/api/v1/trending/`

### **1. Health Check Endpoint**
```http
GET /health
```
**Purpose**: Check if the service is running
**Response**: `{"status": "healthy", "service": "Mirror API"}`

### **2. Get Available Platforms**
```http
GET /platforms
```
**Purpose**: List all available data sources
**Response**: List of platforms with capabilities

### **3. Analyze Trending Topics**
```http
POST /analyze
```
**Request Body**:
```json
{
    "query": "Python machine learning",
    "platforms": ["github", "twitter", "reddit"],
    "max_results_per_platform": 20
}
```

**Response**:
```json
{
    "success": true,
    "message": "Successfully analyzed trending topic: Python machine learning",
    "data": {
        "topic": "Python machine learning",
        "overall_score": 75.5,
        "github_data": [...],
        "twitter_data": [...],
        "reddit_data": [...]
    }
}
```

### **4. Quick Analysis**
```http
POST /quick-analysis
```
**Purpose**: Faster analysis with minimal configuration
**Response**: Summary data without detailed breakdowns

---

## 🗄️ **Database Models & Data Structures**

### **Core Data Models:**

#### **1. TrendingTopic Model**
```python
# backend/models/trending.py
class TrendingTopic(BaseModel):
    topic: str                           # Search topic
    query: str                           # Original search query
    platforms: List[PlatformType]        # Selected platforms
    github_data: Optional[List[GitHubRepo]] = []
    twitter_data: Optional[List[TwitterPost]] = []
    reddit_data: Optional[List[RedditPost]] = []
    analysis_timestamp: datetime         # When analysis was performed
    overall_score: Optional[float]       # Calculated trending score
```

#### **2. GitHub Repository Model**
```python
class GitHubRepo(BaseModel):
    name: str                            # Repository name
    full_name: str                       # Owner/repo-name
    description: Optional[str]           # Repository description
    html_url: str                        # GitHub URL
    stargazers_count: int                # Number of stars
    forks_count: int                     # Number of forks
    language: Optional[str]              # Primary language
    topics: List[str] = []               # Repository topics
    created_at: datetime                 # Creation date
    updated_at: datetime                 # Last update
    open_issues_count: int               # Open issues
    contributors_count: Optional[int]    # Number of contributors
    commits_count: Optional[int]         # Number of commits
    tech_stack: List[str] = []          # Technology stack
```

#### **3. Twitter Post Model**
```python
class TwitterPost(BaseModel):
    id: str                              # Tweet ID
    text: str                            # Tweet content
    author_id: str                       # Author user ID
    author_username: str                 # Author username
    created_at: datetime                 # Tweet creation time
    retweet_count: int                   # Retweet count
    like_count: int                      # Like count
    reply_count: int                     # Reply count
    quote_count: int                     # Quote count
    hashtags: List[str] = []             # Hashtags used
    mentions: List[str] = []             # User mentions
```

#### **4. Reddit Post Model**
```python
class RedditPost(BaseModel):
    id: str                              # Post ID
    title: str                           # Post title
    selftext: str                        # Post content
    author: str                          # Author username
    subreddit: str                       # Subreddit name
    score: int                           # Upvotes - downvotes
    upvote_ratio: float                  # Upvote percentage
    num_comments: int                    # Comment count
    created_utc: datetime                # Creation time
    url: str                             # Post URL
    is_self: bool                        # Is text post
    domain: str                          # Domain (usually reddit.com)
```

---

## ⚙️ **Service Layer Architecture**

### **Service Responsibilities:**

#### **1. GitHub Service (`github_service.py`)**
**Purpose**: Collect and analyze GitHub repository data

**Key Methods**:
```python
def search_trending_repos(query: str, max_results: int) -> List[GitHubRepo]
def get_trending_languages(repos: List[GitHubRepo]) -> List[Dict]
def get_top_contributors(repos: List[GitHubRepo]) -> List[Dict]
```

**How It Works**:
1. **Authentication**: Uses GitHub token for API access
2. **Search**: Queries GitHub API with search criteria
3. **Enrichment**: Fetches additional repository details
4. **Analysis**: Calculates language and contributor statistics

#### **2. Twitter Service (`twitter_service.py`)**
**Purpose**: Collect and analyze Twitter/X post data

**Key Methods**:
```python
def search_trending_posts(query: str, max_results: int) -> List[TwitterPost]
def get_engagement_metrics(posts: List[TwitterPost]) -> Dict
```

**How It Works**:
1. **Authentication**: Uses Twitter API credentials
2. **Search**: Queries Twitter API for relevant posts
3. **Parsing**: Extracts hashtags, mentions, and engagement metrics
4. **Fallback**: Provides mock data if API unavailable

#### **3. Reddit Service (`reddit_service.py`)**
**Purpose**: Collect and analyze Reddit post data

**Key Methods**:
```python
def search_trending_posts(query: str, max_results: int) -> List[RedditPost]
def get_community_metrics(posts: List[RedditPost]) -> Dict
def get_trending_keywords(posts: List[RedditPost]) -> List[Dict]
```

**How It Works**:
1. **Authentication**: Uses Reddit API credentials
2. **Multi-subreddit Search**: Searches across tech subreddits
3. **Community Analysis**: Analyzes engagement and sentiment
4. **Keyword Extraction**: Identifies trending topics and discussions

#### **4. Trending Analyzer (`trending_analyzer.py`)**
**Purpose**: Orchestrate data collection and calculate overall scores

**Key Methods**:
```python
async def analyze_trending_topic(request: TrendingAnalysisRequest) -> TrendingTopic
def _calculate_overall_score(trending_topic: TrendingTopic) -> float
def generate_analysis_summary(trending_topic: TrendingTopic) -> AnalysisSummary
```

**How It Works**:
1. **Coordination**: Manages concurrent data collection from all platforms
2. **Scoring**: Calculates platform-specific and overall trending scores
3. **Summary**: Generates comprehensive analysis reports
4. **Error Handling**: Manages failures gracefully

---

## 🎨 **Frontend Architecture**

### **Component Structure:**

#### **1. App Component (`App.js`)**
**Purpose**: Main application container and routing

```javascript
function App() {
    return (
        <Router>
            <div className="App min-h-screen bg-gray-50">
                <Header />
                <main className="pt-16">
                    <Routes>
                        <Route path="/" element={<HomePage />} />
                        <Route path="/analyze" element={<AnalysisPage />} />
                        <Route path="/results" element={<ResultsPage />} />
                    </Routes>
                </main>
                <Toaster />
            </div>
        </Router>
    );
}
```

#### **2. Page Components**
**Location**: `frontend/src/pages/`

- **HomePage**: Landing page with features and examples
- **AnalysisPage**: Query input and platform selection
- **ResultsPage**: Data visualization and analysis results

#### **3. Reusable Components**
**Location**: `frontend/src/components/`

- **Header**: Navigation and branding
- **Charts**: Data visualization components
- **Cards**: Information display components

### **State Management:**
```javascript
// Local state for form data
const [query, setQuery] = useState('');
const [selectedPlatforms, setSelectedPlatforms] = useState(['github', 'twitter', 'reddit']);
const [isAnalyzing, setIsAnalyzing] = useState(false);

// API calls using axios
const response = await axios.post('/api/v1/trending/analyze', {
    query: query.trim(),
    platforms: selectedPlatforms,
    max_results_per_platform: 20
});
```

### **Styling System:**
```css
/* Tailwind CSS classes */
.btn-primary {
    @apply bg-primary-600 hover:bg-primary-700 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200;
}

.card {
    @apply bg-white rounded-xl shadow-sm border border-gray-200 p-6;
}
```

---

## 🧮 **Trending Algorithm Explained**

### **Overall Score Calculation:**

#### **Formula:**
```
Overall Score = (GitHub_Score × 0.4) + (Twitter_Score × 0.35) + (Reddit_Score × 0.25)
```

#### **Platform Weights:**
- **GitHub**: 40% (Most important - code repositories)
- **Twitter**: 35% (Social engagement and discussions)
- **Reddit**: 25% (Community discussions and sentiment)

### **GitHub Score Calculation (40% weight):**

#### **Metrics Used:**
1. **Stars (50% of GitHub score)**: Repository popularity
2. **Forks (30% of GitHub score)**: Repository adoption
3. **Contributors (20% of GitHub score)**: Community involvement

#### **Formula:**
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

#### **Example Calculation:**
```
Repository 1: 500 stars, 100 forks, 10 contributors
Repository 2: 300 stars, 50 forks, 5 contributors
Repository 3: 200 stars, 25 forks, 3 contributors

Total: 1000 stars, 175 forks, 18 contributors
Average: 333.3 stars, 58.3 forks, 6 contributors

GitHub Score = (333.3 × 0.5) + (58.3 × 0.3) + (6 × 0.2)
             = 166.65 + 17.49 + 1.2
             = 185.34

Normalized Score = min(185.34 / 1000, 100.0) = 18.53
```

### **Twitter Score Calculation (35% weight):**

#### **Metrics Used:**
- **Likes**: User interest and engagement
- **Retweets**: Content sharing and virality
- **Replies**: Discussion and interaction

#### **Formula:**
```python
def _calculate_twitter_score(self, posts: List) -> float:
    total_likes = sum(post.like_count for post in posts)
    total_retweets = sum(post.retweet_count for post in posts)
    total_replies = sum(post.reply_count for post in posts)
    
    total_engagement = total_likes + total_retweets + total_replies
    avg_engagement = total_engagement / len(posts)
    
    return min(avg_engagement / 100, 100.0)
```

### **Reddit Score Calculation (25% weight):**

#### **Metrics Used:**
- **Score (70% of Reddit score)**: Upvotes - downvotes
- **Comments (30% of Reddit score)**: Discussion activity

#### **Formula:**
```python
def _calculate_reddit_score(self, posts: List) -> float:
    total_score = sum(post.score for post in posts)
    total_comments = sum(post.num_comments for post in posts)
    
    avg_score = total_score / len(posts)
    avg_comments = total_comments / len(posts)
    
    score = (avg_score * 0.7) + (avg_comments * 0.3)
    
    return min(score / 100, 100.0)
```

### **Final Score Example:**
```
GitHub Score: 18.53 (out of 100)
Twitter Score: 45.0 (out of 100)
Reddit Score: 70.0 (out of 100)

Overall Score = (18.53 × 0.4) + (45.0 × 0.35) + (70.0 × 0.25)
              = 7.41 + 15.75 + 17.5
              = 40.66
```

---

## 🔧 **How to Make Changes**

### **1. Adding New Platforms**

#### **Step 1: Create Platform Service**
```python
# backend/services/new_platform_service.py
class NewPlatformService:
    def __init__(self):
        self.api_key = settings.NEW_PLATFORM_API_KEY
    
    def search_trending_posts(self, query: str, max_results: int) -> List[NewPlatformPost]:
        # Implementation here
        pass
    
    def get_engagement_metrics(self, posts: List[NewPlatformPost]) -> Dict:
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
    NEW_PLATFORM = "new_platform"  # Add this
```

#### **Step 3: Create Data Model**
```python
# backend/models/trending.py
class NewPlatformPost(BaseModel):
    id: str
    content: str
    author: str
    engagement_score: float
    created_at: datetime
```

#### **Step 4: Integrate with Analyzer**
```python
# backend/services/trending_analyzer.py
async def _collect_new_platform_data(self, query: str, max_results: int) -> List:
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        return await loop.run_in_executor(
            executor, 
            self.new_platform_service.search_trending_posts, 
            query, 
            max_results
        )

def _calculate_new_platform_score(self, posts: List) -> float:
    # Implement scoring logic
    pass
```

#### **Step 5: Update Frontend**
```javascript
// frontend/src/pages/AnalysisPage.js
const platforms = [
    // ... existing platforms
    {
        id: 'new_platform',
        name: 'New Platform',
        description: 'Description here',
        icon: NewPlatformIcon,
        color: 'from-purple-500 to-purple-700'
    }
];
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

#### **Step 1: Create Route**
```python
# backend/api/routes.py
@trending_router.get("/trending-history")
async def get_trending_history():
    """Get historical trending data"""
    return {"message": "Historical data endpoint"}
```

#### **Step 2: Add Frontend Integration**
```javascript
// frontend/src/pages/ResultsPage.js
const fetchTrendingHistory = async () => {
    const response = await axios.get('/api/v1/trending/trending-history');
    // Handle response
};
```

### **4. Modifying Data Models**

#### **Add New Fields:**
```python
# backend/models/trending.py
class GitHubRepo(BaseModel):
    # Existing fields...
    new_field: Optional[str] = None
    another_field: Optional[int] = None
```

#### **Update Service Layer:**
```python
# backend/services/github_service.py
def _enrich_repo_data(self, repo) -> GitHubRepo:
    return GitHubRepo(
        # Existing fields...
        new_field=self._extract_new_field(repo),
        another_field=self._calculate_another_field(repo)
    )
```

### **5. Adding New Visualizations**

#### **Step 1: Create Chart Component**
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

#### **Step 2: Integrate in Results Page**
```javascript
// frontend/src/pages/ResultsPage.js
import NewChart from '../components/NewChart';

const renderNewChart = () => (
    <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">New Visualization</h3>
        <NewChart data={chartData} />
    </div>
);
```

---

## 🚨 **Troubleshooting Guide**

### **Common Issues and Solutions:**

#### **1. Backend Won't Start**

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

**Problem**: Port 8000 already in use
**Solution**: Kill existing process
```bash
lsof -i :8000
kill -9 <PID>
```

#### **2. Frontend Won't Start**

**Problem**: `npm start` fails
**Solution**: Clear cache and reinstall
```bash
rm -rf node_modules package-lock.json
npm install
npm start
```

**Problem**: Port 3000 already in use
**Solution**: Use different port
```bash
PORT=3001 npm start
```

#### **3. API Calls Failing**

**Problem**: 401 Unauthorized errors
**Solution**: Check API keys in `.env` file
```bash
cat .env
# Verify GITHUB_TOKEN, TWITTER_API_KEY, etc.
```

**Problem**: Rate limiting errors
**Solution**: Add delays in service calls
```python
import time
time.sleep(0.1)  # Add 100ms delay between API calls
```

#### **4. Data Not Loading**

**Problem**: Empty results
**Solution**: Check API responses
```python
# Add logging in services
print(f"API Response: {response}")
```

**Problem**: Mock data showing instead of real data
**Solution**: Verify API credentials and connectivity
```bash
curl -H "Authorization: token YOUR_GITHUB_TOKEN" \
     https://api.github.com/user
```

#### **5. Frontend-Backend Connection Issues**

**Problem**: Proxy errors
**Solution**: Check backend is running
```bash
curl http://localhost:8000/health
```

**Problem**: CORS errors
**Solution**: Verify CORS configuration in backend
```python
# backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### **Debugging Techniques:**

#### **1. Backend Logging**
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def search_trending_repos(self, query: str, max_results: int = 20):
    logger.debug(f"Searching GitHub for: {query}")
    # ... rest of the code
```

#### **2. Frontend Console Logging**
```javascript
console.log('API Response:', response.data);
console.log('Analysis Data:', analysisData);
```

#### **3. API Testing with curl**
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test analysis endpoint
curl -X POST "http://localhost:8000/api/v1/trending/analyze" \
     -H "Content-Type: application/json" \
     -d '{"query": "test", "platforms": ["github"], "max_results_per_platform": 5}'
```

---

## 🎯 **Next Steps & Advanced Features**

### **Potential Enhancements:**

1. **Database Integration**: Store analysis results for historical tracking
2. **Caching**: Implement Redis for API response caching
3. **Real-time Updates**: WebSocket integration for live data
4. **Machine Learning**: AI-powered trend prediction
5. **Export Features**: PDF reports, CSV data export
6. **User Accounts**: Save favorite searches and analysis history
7. **Notifications**: Alert users when topics become trending
8. **API Rate Limiting**: Implement proper rate limiting for external APIs

### **Performance Optimizations:**

1. **Async Processing**: Already implemented with asyncio
2. **Connection Pooling**: Reuse API connections
3. **Data Compression**: Compress API responses
4. **CDN Integration**: Serve static assets from CDN
5. **Database Indexing**: Optimize database queries

---

## 📚 **Additional Resources**

### **Documentation:**
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://reactjs.org/docs/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Recharts Documentation](https://recharts.org/)

### **API References:**
- [GitHub API](https://docs.github.com/en/rest)
- [Twitter API](https://developer.twitter.com/en/docs)
- [Reddit API](https://www.reddit.com/dev/api/)

### **Development Tools:**
- **Postman**: API testing and development
- **Insomnia**: Alternative to Postman
- **Chrome DevTools**: Frontend debugging
- **Python Debugger**: Backend debugging

---

## 🎉 **Congratulations!**

You now have a **deep understanding** of the Mirror project architecture and can confidently make changes to:

- ✅ **Add new platforms** and data sources
- ✅ **Modify trending algorithms** and scoring
- ✅ **Create new API endpoints** and features
- ✅ **Customize data models** and structures
- ✅ **Add new visualizations** and charts
- ✅ **Debug issues** and optimize performance

The Mirror project is designed to be **modular and extensible**, so you can easily add new features while maintaining the existing architecture. Happy coding! 🚀✨
