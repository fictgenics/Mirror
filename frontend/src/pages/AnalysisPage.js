import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { 
  Search, 
  Github, 
  Twitter, 
  MessageCircle, 
  TrendingUp,
  BarChart3,
  Loader2,
  CheckCircle,
  AlertCircle
} from 'lucide-react';
import toast from 'react-hot-toast';
import axios from 'axios';

const AnalysisPage = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [query, setQuery] = useState('');
  const [selectedPlatforms, setSelectedPlatforms] = useState(['github', 'twitter', 'reddit']);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisProgress, setAnalysisProgress] = useState(0);

  const platforms = [
    {
      id: 'github',
      name: 'GitHub',
      description: 'Repository analysis, languages, contributors',
      icon: Github,
      color: 'from-gray-500 to-gray-700'
    },
    {
      id: 'twitter',
      name: 'Twitter/X',
      description: 'Trending posts, engagement metrics',
      icon: Twitter,
      color: 'from-blue-400 to-blue-600'
    },
    {
      id: 'reddit',
      name: 'Reddit',
      description: 'Community discussions, sentiment analysis',
      icon: MessageCircle,
      color: 'from-orange-400 to-orange-600'
    }
  ];

  useEffect(() => {
    // Pre-fill query from URL params
    const queryParam = searchParams.get('query');
    if (queryParam) {
      setQuery(queryParam);
    }
  }, [searchParams]);

  const handlePlatformToggle = (platformId) => {
    setSelectedPlatforms(prev => 
      prev.includes(platformId)
        ? prev.filter(id => id !== platformId)
        : [...prev, platformId]
    );
  };

  const validateForm = () => {
    if (!query.trim()) {
      toast.error('Please enter a search query');
      return false;
    }
    if (selectedPlatforms.length === 0) {
      toast.error('Please select at least one platform');
      return false;
    }
    return true;
  };

  const startAnalysis = async () => {
    if (!validateForm()) return;

    setIsAnalyzing(true);
    setAnalysisProgress(0);

    try {
      // Simulate progress updates
      const progressInterval = setInterval(() => {
        setAnalysisProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 500);

      const response = await axios.post('/api/v1/trending/analyze', {
        query: query.trim(),
        platforms: selectedPlatforms,
        max_results_per_platform: 20
      });

      clearInterval(progressInterval);
      setAnalysisProgress(100);

      if (response.data.success) {
        toast.success('Analysis completed successfully!');
        // Navigate to results page with data
        navigate('/results', { 
          state: { 
            analysisData: response.data.data,
            query: query.trim()
          }
        });
      } else {
        throw new Error(response.data.error || 'Analysis failed');
      }

    } catch (error) {
      console.error('Analysis error:', error);
      toast.error(error.response?.data?.error || 'Analysis failed. Please try again.');
    } finally {
      setIsAnalyzing(false);
      setAnalysisProgress(0);
    }
  };

  const handleQuickAnalysis = async () => {
    if (!query.trim()) {
      toast.error('Please enter a search query');
      return;
    }

    setIsAnalyzing(true);
    try {
      const response = await axios.post('/api/v1/trending/quick-analysis', {
        query: query.trim()
      });

      if (response.data.success) {
        toast.success('Quick analysis completed!');
        navigate('/results', { 
          state: { 
            analysisData: response.data,
            query: query.trim(),
            isQuickAnalysis: true
          }
        });
      } else {
        throw new Error(response.data.error || 'Quick analysis failed');
      }

    } catch (error) {
      console.error('Quick analysis error:', error);
      toast.error('Quick analysis failed. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Analyze Trending Topics
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Discover what's trending across multiple platforms with comprehensive data analysis and visualization
          </p>
        </div>

        {/* Analysis Form */}
        <div className="card mb-8">
          <div className="mb-6">
            <label htmlFor="query" className="block text-sm font-medium text-gray-700 mb-2">
              What would you like to analyze?
            </label>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                id="query"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="e.g., Python machine learning, JavaScript frameworks, Data science tools..."
                className="input-field pl-10 text-lg"
                disabled={isAnalyzing}
              />
            </div>
          </div>

          {/* Platform Selection */}
          <div className="mb-8">
            <label className="block text-sm font-medium text-gray-700 mb-4">
              Select platforms to analyze:
            </label>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {platforms.map((platform) => {
                const Icon = platform.icon;
                const isSelected = selectedPlatforms.includes(platform.id);
                return (
                  <button
                    key={platform.id}
                    onClick={() => handlePlatformToggle(platform.id)}
                    disabled={isAnalyzing}
                    className={`p-4 rounded-lg border-2 transition-all duration-200 ${
                      isSelected
                        ? 'border-primary-500 bg-primary-50'
                        : 'border-gray-200 hover:border-gray-300 bg-white'
                    } ${isAnalyzing ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
                  >
                    <div className={`w-12 h-12 mx-auto mb-3 rounded-lg bg-gradient-to-br ${platform.color} flex items-center justify-center`}>
                      <Icon className="w-6 h-6 text-white" />
                    </div>
                    <h3 className="font-semibold text-gray-900 mb-1">
                      {platform.name}
                    </h3>
                    <p className="text-sm text-gray-600">
                      {platform.description}
                    </p>
                    {isSelected && (
                      <CheckCircle className="w-5 h-5 text-primary-500 mx-auto mt-2" />
                    )}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-4">
            <button
              onClick={startAnalysis}
              disabled={isAnalyzing || selectedPlatforms.length === 0}
              className="btn-primary flex-1 py-3 text-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isAnalyzing ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin mr-2" />
                  Analyzing...
                </>
              ) : (
                <>
                  <BarChart3 className="w-5 h-5 mr-2" />
                  Start Full Analysis
                </>
              )}
            </button>
            
            <button
              onClick={handleQuickAnalysis}
              disabled={isAnalyzing || !query.trim()}
              className="btn-secondary flex-1 py-3 text-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isAnalyzing ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin mr-2" />
                  Analyzing...
                </>
              ) : (
                <>
                  <TrendingUp className="w-5 h-5 mr-2" />
                  Quick Analysis
                </>
              )}
            </button>
          </div>
        </div>

        {/* Progress Bar */}
        {isAnalyzing && (
          <div className="card">
            <div className="mb-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-gray-700">Analysis Progress</span>
                <span className="text-sm text-gray-500">{analysisProgress}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-primary-600 h-2 rounded-full transition-all duration-300 ease-out"
                  style={{ width: `${analysisProgress}%` }}
                ></div>
              </div>
            </div>
            <div className="text-center text-sm text-gray-600">
              <Loader2 className="w-4 h-4 animate-spin inline mr-2" />
              Collecting data from {selectedPlatforms.length} platform{selectedPlatforms.length !== 1 ? 's' : ''}...
            </div>
          </div>
        )}

        {/* Tips */}
        <div className="card bg-blue-50 border-blue-200">
          <div className="flex items-start space-x-3">
            <AlertCircle className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
            <div>
              <h3 className="font-medium text-blue-900 mb-1">Analysis Tips</h3>
              <ul className="text-sm text-blue-800 space-y-1">
                <li>• Be specific with your query for better results</li>
                <li>• Select multiple platforms for comprehensive analysis</li>
                <li>• Use "Quick Analysis" for faster results with basic insights</li>
                <li>• Full analysis provides detailed data and visualizations</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalysisPage;
