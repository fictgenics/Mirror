#!/usr/bin/env python3
"""
Simple test script to verify Mirror backend setup
"""

import requests
import json
from datetime import datetime

def test_backend():
    """Test basic backend functionality"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Mirror Backend...")
    print("=" * 50)
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server")
        print("   Make sure the backend is running on http://localhost:8000")
        return False
    
    # Test platforms endpoint
    try:
        response = requests.get(f"{base_url}/api/v1/trending/platforms")
        if response.status_code == 200:
            print("✅ Platforms endpoint working")
            platforms = response.json()
            print(f"   Available platforms: {len(platforms['platforms'])}")
        else:
            print(f"❌ Platforms endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing platforms endpoint: {e}")
    
    # Test example queries endpoint
    try:
        response = requests.get(f"{base_url}/api/v1/trending/example-queries")
        if response.status_code == 200:
            print("✅ Example queries endpoint working")
            queries = response.json()
            print(f"   Available example queries: {len(queries['example_queries'])}")
        else:
            print(f"❌ Example queries endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing example queries endpoint: {e}")
    
    print("\n🎯 Backend is ready for analysis!")
    print("\n📝 Next steps:")
    print("   1. Configure your API keys in .env file")
    print("   2. Start the frontend: ./start_frontend.sh")
    print("   3. Visit http://localhost:3000 to use the web interface")
    
    return True

if __name__ == "__main__":
    test_backend()
