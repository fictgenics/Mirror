import React from 'react';
import { Link } from 'react-router-dom';
import { 
  Search, 
  BarChart3, 
  TrendingUp, 
  Github, 
  ArrowRight,
  Zap,
  Shield,
  Globe
} from 'lucide-react';

const HomePage = () => {
  const features = [
    {
      icon: Github,
      title: 'GitHub Analysis',
      description: 'Analyze trending repositories, programming languages, and contributor activity across the GitHub ecosystem.',
      color: 'from-gray-500 to-gray-700'
    }
  ];

  const benefits = [
    {
      icon: TrendingUp,
      title: 'Real-time Trends',
      description: 'Get up-to-date information on what\'s trending across multiple platforms simultaneously.'
    },
    {
      icon: BarChart3,
      title: 'Data Visualization',
      description: 'Beautiful charts and graphs to understand trends, patterns, and insights at a glance.'
    },
    {
      icon: Zap,
      title: 'Fast Analysis',
      description: 'Quick analysis with our optimized algorithms that process data from multiple sources efficiently.'
    },
    {
      icon: Shield,
      title: 'Reliable Data',
      description: 'Data sourced directly from official APIs ensuring accuracy and reliability of information.'
    }
  ];

  const exampleQueries = [
    'Python machine learning',
    'JavaScript frameworks',
    'Data science tools',
    'Web development trends',
    'Open source projects'
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-primary-50 via-white to-accent-50 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
              Discover What's{' '}
              <span className="text-gradient">Trending</span>
            </h1>
            <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
              Analyze trending topics across GitHub with powerful data visualization and insights. 
              Stay ahead of the curve in technology and development.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/analyze"
                className="btn-primary text-lg px-8 py-3 flex items-center justify-center space-x-2"
              >
                <Search className="w-5 h-5" />
                <span>Start Analyzing</span>
                <ArrowRight className="w-5 h-5" />
              </Link>
              <button className="btn-secondary text-lg px-8 py-3">
                View Examples
              </button>
            </div>
          </div>
        </div>
        
        {/* Background decoration */}
        <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-primary-200 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-pulse-slow"></div>
          <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-accent-200 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-pulse-slow"></div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              GitHub Repository Analysis
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Get comprehensive insights by analyzing trending repositories, languages, and contributors on GitHub
            </p>
          </div>
          
          <div className="grid-responsive">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <div key={index} className="card card-hover text-center">
                  <div className={`w-16 h-16 mx-auto mb-6 rounded-xl bg-gradient-to-br ${feature.color} flex items-center justify-center`}>
                    <Icon className="w-8 h-8 text-white" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">
                    {feature.title}
                  </h3>
                  <p className="text-gray-600">
                    {feature.description}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Why Choose Mirror?
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Powerful features that make trend analysis simple, fast, and insightful
            </p>
          </div>
          
          <div className="grid-responsive">
            {benefits.map((benefit, index) => {
              const Icon = benefit.icon;
              return (
                <div key={index} className="card card-hover">
                  <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
                    <Icon className="w-6 h-6 text-primary-600" />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    {benefit.title}
                  </h3>
                  <p className="text-gray-600">
                    {benefit.description}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Example Queries Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Popular Analysis Topics
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Try these trending topics to see Mirror in action
            </p>
          </div>
          
          <div className="grid-responsive">
            {exampleQueries.map((query, index) => (
              <div key={index} className="card card-hover text-center">
                <div className="w-12 h-12 bg-accent-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <Search className="w-6 h-6 text-accent-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">
                  {query}
                </h3>
                <Link
                  to={`/analyze?query=${encodeURIComponent(query)}`}
                  className="btn-primary inline-flex items-center space-x-2"
                >
                  <span>Analyze</span>
                  <ArrowRight className="w-4 h-4" />
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-primary-600 to-accent-600">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
            Ready to Discover Trends?
          </h2>
          <p className="text-xl text-primary-100 mb-8">
            Start analyzing trending topics across multiple platforms and get insights that matter
          </p>
          <Link
            to="/analyze"
            className="bg-white text-primary-600 hover:bg-gray-100 font-semibold py-3 px-8 rounded-lg text-lg transition-colors duration-200 inline-flex items-center space-x-2"
          >
            <span>Get Started Now</span>
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
