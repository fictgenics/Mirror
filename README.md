# Mirror - Trending Topics Analyzer 🔍

Mirror is a comprehensive platform that analyzes trending topics across multiple platforms including GitHub, Twitter/X, and Reddit. It provides powerful data visualization and insights to help you understand what's trending in the tech world.

## ✨ Features

- **Multi-Platform Analysis**: Analyze trends across GitHub, Twitter/X, and Reddit simultaneously
- **Real-time Data**: Get up-to-date information from official APIs
- **Beautiful Visualizations**: Interactive charts and graphs using Chart.js and Recharts
- **Comprehensive Insights**: Repository analysis, engagement metrics, community sentiment
- **Modern UI**: Beautiful, responsive interface built with React and Tailwind CSS
- **Fast Performance**: Optimized backend with async processing and caching

## 🏗️ Architecture

```
Mirror/
├── backend/                 # FastAPI backend
│   ├── api/                # API routes and endpoints
│   ├── core/               # Configuration and core utilities
│   ├── models/             # Pydantic data models
│   ├── services/           # Business logic services
│   └── utils/              # Utility functions
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Page components
│   │   ├── utils/          # Utility functions
│   │   └── styles/         # CSS and styling
│   └── public/             # Static assets
├── data_analysis/          # Data analysis scripts
├── docs/                   # Documentation
└── tests/                  # Test files
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- API keys for GitHub, Twitter/X, and Reddit

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Mirror
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your API keys
   ```

5. **Run the backend**
   ```bash
   cd backend
   python main.py
   ```

### Frontend Setup

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server**
   ```bash
   npm start
   ```

3. **Build for production**
   ```bash
   npm run build
   ```

## 🔑 API Configuration

### GitHub API
- Get a Personal Access Token from [GitHub Settings](https://github.com/settings/tokens)
- Add to `.env`: `GITHUB_TOKEN=your_token_here`

### Twitter/X API
- Apply for API access at [Twitter Developer Portal](https://developer.twitter.com/)
- Add to `.env`:
  ```
  TWITTER_API_KEY=your_api_key
  TWITTER_API_SECRET=your_api_secret
  TWITTER_ACCESS_TOKEN=your_access_token
  TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
  TWITTER_BEARER_TOKEN=your_bearer_token
  ```

### Reddit API
- Create an app at [Reddit Apps](https://www.reddit.com/prefs/apps)
- Add to `.env`:
  ```
  REDDIT_CLIENT_ID=your_client_id
  REDDIT_CLIENT_SECRET=your_client_secret
  REDDIT_USER_AGENT=MirrorTrendingAnalyzer/1.0
  ```

## 📊 Usage Examples

### Analyze Python Machine Learning Trends
```bash
curl -X POST "http://localhost:8000/api/v1/trending/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Python machine learning",
    "platforms": ["github", "twitter", "reddit"],
    "max_results_per_platform": 20
  }'
```

### Quick Analysis
```bash
curl -X POST "http://localhost:8000/api/v1/trending/quick-analysis" \
  -H "Content-Type: application/json" \
  -d '{"query": "JavaScript frameworks"}'
```

## 🎯 What You Can Analyze

### GitHub Insights
- Trending repositories by stars and forks
- Programming language popularity
- Contributor activity and engagement
- Repository topics and tech stack
- Creation and update patterns

### Twitter/X Insights
- Trending posts and hashtags
- Engagement metrics (likes, retweets, replies)
- User sentiment and discussions
- Hashtag frequency analysis
- Post performance trends

### Reddit Insights
- Community discussions and sentiment
- Post scores and upvote ratios
- Subreddit activity patterns
- Keyword frequency analysis
- Community engagement metrics

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Python 3.8+**: Core programming language
- **Pydantic**: Data validation and settings management
- **GitHub3.py**: GitHub API client
- **Tweepy**: Twitter API client
- **PRAW**: Reddit API client
- **Uvicorn**: ASGI server

### Frontend
- **React 18**: Modern React with hooks and functional components
- **Tailwind CSS**: Utility-first CSS framework
- **Recharts**: Composable charting library
- **React Router**: Client-side routing
- **Axios**: HTTP client for API calls
- **Lucide React**: Beautiful icon library
- **Framer Motion**: Animation library

### Data Analysis
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Matplotlib**: Plotting and visualization
- **Seaborn**: Statistical data visualization

## 📈 Data Visualization

Mirror provides comprehensive data visualization including:

- **Bar Charts**: Language distribution, engagement metrics
- **Line Charts**: Trend analysis over time
- **Pie Charts**: Platform data distribution
- **Interactive Dashboards**: Real-time data exploration
- **Responsive Design**: Works on all device sizes

## 🔒 Security Features

- Environment variable configuration for API keys
- Rate limiting and API quota management
- Input validation and sanitization
- CORS configuration for frontend-backend communication
- Error handling and logging

## 🧪 Testing

```bash
# Run backend tests
cd backend
python -m pytest

# Run frontend tests
cd frontend
npm test
```

## 📝 API Documentation

Once the backend is running, visit:
- **Interactive API docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health check**: http://localhost:8000/health

## 🚀 Deployment

### Backend Deployment
```bash
# Using Docker
docker build -t mirror-backend .
docker run -p 8000:8000 mirror-backend

# Using production server
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend Deployment
```bash
# Build production bundle
npm run build

# Deploy to static hosting (Netlify, Vercel, etc.)
# or serve from backend static files
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- GitHub, Twitter/X, and Reddit for their APIs
- The open-source community for amazing libraries
- Contributors and users of Mirror

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/mirror/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/mirror/discussions)
- **Email**: support@mirror-analyzer.com

---

**Mirror** - See what's trending across the tech world! 🚀
