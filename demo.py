#!/usr/bin/env python
"""
Demo script to showcase the Government Voice Chatbot capabilities
Run this after starting the server to see the chatbot in action
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def print_banner():
    print("=" * 70)
    print("🎯 Government Voice Chatbot - API Demo")
    print("=" * 70)

def test_text_chat():
    """Test text-based chat functionality"""
    print("\n📝 Testing Text Chat API...")
    
    test_queries = [
        "What are agriculture schemes available?",
        "Tell me about health schemes for women",
        "How to apply for education scholarships?",
        "What benefits do employment schemes provide?"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: {query}")
        
        try:
            response = requests.post(f"{BASE_URL}/api/chat/text/", 
                json={"query": query, "language": "en"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    print(f"✅ Response: {data['response'][:150]}...")
                    print(f"   Intent: {data['intent']}")
                    print(f"   Schemes found: {data['scheme_count']}")
                    print(f"   Confidence: {data['confidence']:.2f}")
                else:
                    print(f"❌ Error: {data.get('error', 'Unknown error')}")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection Error: {e}")
        
        time.sleep(1)  # Rate limiting

def test_scheme_search():
    """Test scheme search API"""
    print("\n🔍 Testing Scheme Search API...")
    
    search_queries = [
        "agriculture",
        "health",
        "education",
        "employment"
    ]
    
    for query in search_queries:
        print(f"\n🔍 Searching for: {query}")
        
        try:
            response = requests.get(f"{BASE_URL}/api/schemes/search/", 
                params={"q": query, "limit": 3},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    print(f"✅ Found {data['scheme_count']} schemes")
                    for i, scheme in enumerate(data['schemes'], 1):
                        print(f"   {i}. {scheme['title']}")
                        print(f"      Sector: {scheme['sector']}")
                else:
                    print(f"❌ Search failed: {data.get('error', 'Unknown error')}")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection Error: {e}")
        
        time.sleep(1)

def test_utility_apis():
    """Test utility APIs"""
    print("\n🛠️ Testing Utility APIs...")
    
    # Test languages API
    try:
        response = requests.get(f"{BASE_URL}/api/schemes/languages/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            languages = [lang['name'] for lang in data['languages']]
            print(f"✅ Supported Languages: {', '.join(languages)}")
        else:
            print(f"❌ Languages API Error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Languages API Connection Error: {e}")
    
    # Test sectors API
    try:
        response = requests.get(f"{BASE_URL}/api/schemes/sectors/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            sectors = [sector['name'] for sector in data['sectors']]
            print(f"✅ Available Sectors: {', '.join(sectors[:5])}...")
        else:
            print(f"❌ Sectors API Error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Sectors API Connection Error: {e}")

def check_server_status():
    """Check if the server is running"""
    print("🔍 Checking server status...")
    
    try:
        response = requests.get(BASE_URL, timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and accessible")
            return True
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to server: {e}")
        print("   Make sure to run: python start.py")
        return False

def main():
    """Run the demo"""
    print_banner()
    
    if not check_server_status():
        print("\n🚨 Please start the server first:")
        print("   python start.py")
        return
    
    print("\n🎉 Server is running! Testing APIs...")
    
    # Run tests
    test_text_chat()
    test_scheme_search()
    test_utility_apis()
    
    print("\n" + "=" * 70)
    print("🎯 Demo completed!")
    print("\n📱 Try the web interface at: http://localhost:8000")
    print("🎤 Test voice input by clicking 'CLICK & SPEAK'")
    print("💬 Test text input by typing in the text box")
    print("🌐 Try different languages using the language selector")
    print("=" * 70)

if __name__ == "__main__":
    main()
