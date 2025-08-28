import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { 
  ArrowLeft, 
  Download, 
  Share2, 
  TrendingUp,
  Github,
  Twitter,
  MessageCircle,
  Star,
  GitFork,
  MessageSquare,
  Heart,
  Repeat2
} from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line } from 'recharts';
import toast from 'react-hot-toast';

const ResultsPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('overview');
  const [analysisData, setAnalysisData] = useState(null);
  const [query, setQuery] = useState('');

  useEffect(() => {
    if (location.state?.analysisData) {
      setAnalysisData(location.state.analysisData);
      setQuery(location.state.query || '');
    } else {
      // No data, redirect to analysis page
      navigate('/analyze');
    }
  }, [location.state, navigate]);

  if (!analysisData) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading results...</p>
        </div>
      </div>
    );
  }

  const tabs = [
    { id: 'overview', name: 'Overview', icon: TrendingUp },
    { id: 'github', name: 'GitHub', icon: Github },
    { id: 'twitter', name: 'Twitter', icon: Twitter },
    { id: 'reddit', name: 'Reddit', icon: MessageCircle }
  ];

  const renderOverviewTab = () => (
    <div className="space-y-6">
      {/* Overall Score */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Overall Trending Score</h3>
        <div className="text-center">
          <div className="text-4xl font-bold text-primary-600 mb-2">
            {analysisData.overall_score ? Math.round(analysisData.overall_score) : 'N/A'}
          </div>
          <div className="text-sm text-gray-500">out of 100</div>
        </div>
      </div>

      {/* Platform Summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {analysisData.github_data && (
          <div className="card">
            <div className="flex items-center space-x-3 mb-4">
              <Github className="w-6 h-6 text-gray-600" />
              <h4 className="font-semibold text-gray-900">GitHub</h4>
            </div>
            <div className="text-2xl font-bold text-gray-900 mb-2">
              {analysisData.github_data.length}
            </div>
            <div className="text-sm text-gray-600">Repositories analyzed</div>
          </div>
        )}

        {analysisData.twitter_data && (
          <div className="card">
            <div className="flex items-center space-x-3 mb-4">
              <Twitter className="w-6 h-6 text-blue-500" />
              <h4 className="font-semibold text-gray-900">Twitter/X</h4>
            </div>
            <div className="text-2xl font-bold text-gray-900 mb-2">
              {analysisData.twitter_data.length}
            </div>
            <div className="text-sm text-gray-600">Posts analyzed</div>
          </div>
        )}

        {analysisData.reddit_data && (
          <div className="card">
            <div className="flex items-center space-x-3 mb-4">
              <MessageCircle className="w-6 h-6 text-orange-500" />
              <h4 className="font-semibold text-gray-900">Reddit</h4>
            </div>
            <div className="text-2xl font-bold text-gray-900 mb-2">
              {analysisData.reddit_data.length}
            </div>
            <div className="text-sm text-gray-600">Posts analyzed</div>
          </div>
        )}
      </div>

      {/* Quick Insights */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Insights</h3>
        <div className="space-y-3">
          <div className="flex items-center space-x-3">
            <div className="w-2 h-2 bg-primary-500 rounded-full"></div>
            <span className="text-gray-700">
              Analysis completed at {new Date(analysisData.analysis_timestamp).toLocaleString()}
            </span>
          </div>
          <div className="flex items-center space-x-3">
            <div className="w-2 h-2 bg-accent-500 rounded-full"></div>
            <span className="text-gray-700">
              Data collected from {analysisData.platforms.length} platform{analysisData.platforms.length !== 1 ? 's' : ''}
            </span>
          </div>
        </div>
      </div>
    </div>
  );

  const renderGitHubTab = () => {
    if (!analysisData.github_data || analysisData.github_data.length === 0) {
      return (
        <div className="card text-center py-12">
          <Github className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600">No GitHub data available</p>
        </div>
      );
    }

    const repos = analysisData.github_data;
    const languageData = repos
      .filter(repo => repo.language)
      .reduce((acc, repo) => {
        acc[repo.language] = (acc[repo.language] || 0) + 1;
        return acc;
      }, {});

    const chartData = Object.entries(languageData)
      .map(([language, count]) => ({ language, count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 10);

    const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D', '#FFC658', '#FF7300', '#00FF00', '#FF0000'];

    return (
      <div className="space-y-6">
        {/* Repository List */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Repositories</h3>
          <div className="space-y-4">
            {repos.slice(0, 10).map((repo, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h4 className="font-medium text-gray-900 mb-1">
                      <a href={repo.html_url} target="_blank" rel="noopener noreferrer" className="hover:text-primary-600">
                        {repo.full_name}
                      </a>
                    </h4>
                    <p className="text-sm text-gray-600 mb-2">{repo.description}</p>
                    <div className="flex items-center space-x-4 text-sm text-gray-500">
                      <span className="flex items-center space-x-1">
                        <Star className="w-4 h-4" />
                        <span>{repo.stargazers_count}</span>
                      </span>
                      <span className="flex items-center space-x-1">
                        <GitFork className="w-4 h-4" />
                        <span>{repo.forks_count}</span>
                      </span>
                      {repo.language && (
                        <span className="px-2 py-1 bg-gray-100 rounded text-xs">
                          {repo.language}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Language Distribution Chart */}
        {chartData.length > 0 && (
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Programming Language Distribution</h3>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="language" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="count" fill="#3b82f6" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}
      </div>
    );
  };

  const renderTwitterTab = () => {
    if (!analysisData.twitter_data || analysisData.twitter_data.length === 0) {
      return (
        <div className="card text-center py-12">
          <Twitter className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600">No Twitter data available</p>
        </div>
      );
    }

    const posts = analysisData.twitter_data;
    const engagementData = posts.map(post => ({
      post: post.author_username,
      likes: post.like_count,
      retweets: post.retweet_count,
      replies: post.reply_count
    })).slice(0, 10);

    return (
      <div className="space-y-6">
        {/* Engagement Chart */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Post Engagement</h3>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={engagementData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="post" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="likes" fill="#3b82f6" name="Likes" />
                <Bar dataKey="retweets" fill="#10b981" name="Retweets" />
                <Bar dataKey="replies" fill="#f59e0b" name="Replies" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Top Posts */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Posts</h3>
          <div className="space-y-4">
            {posts.slice(0, 10).map((post, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <p className="text-gray-900 mb-2">{post.text}</p>
                    <div className="flex items-center space-x-4 text-sm text-gray-500">
                      <span className="flex items-center space-x-1">
                        <Heart className="w-4 h-4" />
                        <span>{post.like_count}</span>
                      </span>
                      <span className="flex items-center space-x-1">
                        <Repeat2 className="w-4 h-4" />
                        <span>{post.retweet_count}</span>
                      </span>
                      <span className="flex items-center space-x-1">
                        <MessageSquare className="w-4 h-4" />
                        <span>{post.reply_count}</span>
                      </span>
                      <span className="text-xs text-gray-400">
                        @{post.author_username}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  const renderRedditTab = () => {
    if (!analysisData.reddit_data || analysisData.reddit_data.length === 0) {
      return (
        <div className="card text-center py-12">
          <MessageCircle className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600">No Reddit data available</p>
        </div>
      );
    }

    const posts = analysisData.reddit_data;
    const scoreData = posts
      .map(post => ({ title: post.title.substring(0, 30) + '...', score: post.score }))
      .sort((a, b) => b.score - a.score)
      .slice(0, 10);

    return (
      <div className="space-y-6">
        {/* Score Distribution */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Post Scores</h3>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={scoreData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="title" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="score" fill="#f59e0b" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Top Posts */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Posts</h3>
          <div className="space-y-4">
            {posts.slice(0, 10).map((post, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h4 className="font-medium text-gray-900 mb-1">
                      <a href={post.url} target="_blank" rel="noopener noreferrer" className="hover:text-primary-600">
                        {post.title}
                      </a>
                    </h4>
                    <p className="text-sm text-gray-600 mb-2">{post.selftext.substring(0, 150)}...</p>
                    <div className="flex items-center space-x-4 text-sm text-gray-500">
                      <span className="px-2 py-1 bg-orange-100 text-orange-800 rounded text-xs">
                        r/{post.subreddit}
                      </span>
                      <span className="flex items-center space-x-1">
                        <TrendingUp className="w-4 h-4" />
                        <span>{post.score}</span>
                      </span>
                      <span className="flex items-center space-x-1">
                        <MessageSquare className="w-4 h-4" />
                        <span>{post.num_comments}</span>
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  const renderTabContent = () => {
    switch (activeTab) {
      case 'overview':
        return renderOverviewTab();
      case 'github':
        return renderGitHubTab();
      case 'twitter':
        return renderTwitterTab();
      case 'reddit':
        return renderRedditTab();
      default:
        return renderOverviewTab();
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-6">
            <button
              onClick={() => navigate('/analyze')}
              className="btn-secondary inline-flex items-center space-x-2"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Back to Analysis</span>
            </button>
            <div className="flex items-center space-x-3">
              <button className="btn-secondary inline-flex items-center space-x-2">
                <Download className="w-4 h-4" />
                <span>Export</span>
              </button>
              <button className="btn-secondary inline-flex items-center space-x-2">
                <Share2 className="w-4 h-4" />
                <span>Share</span>
              </button>
            </div>
          </div>
          
          <div className="text-center">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Analysis Results
            </h1>
            <p className="text-xl text-gray-600">
              "{query}" across multiple platforms
            </p>
          </div>
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 mb-8">
          <div className="border-b border-gray-200">
            <nav className="flex space-x-8 px-6" aria-label="Tabs">
              {tabs.map((tab) => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`py-4 px-1 border-b-2 font-medium text-sm flex items-center space-x-2 ${
                      activeTab === tab.id
                        ? 'border-primary-500 text-primary-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    <span>{tab.name}</span>
                  </button>
                );
              })}
            </nav>
          </div>
        </div>

        {/* Tab Content */}
        <div className="animate-fade-in">
          {renderTabContent()}
        </div>
      </div>
    </div>
  );
};

export default ResultsPage;
