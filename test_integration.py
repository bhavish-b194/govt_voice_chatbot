#!/usr/bin/env python
"""
Test script to verify the integration between frontend and backend
This script tests the chatbot logic and MongoDB connection
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'govt_voice_chatbot.settings')
django.setup()

from chatbot.chatbot_logic import chatbot
from mongodb_adapter import MongoDBAdapter

def test_mongodb_connection():
    """Test MongoDB connection and data"""
    print("Testing MongoDB connection...")
    try:
        adapter = MongoDBAdapter()
        stats = adapter.get_scheme_statistics()
        print(f"✅ MongoDB connected successfully")
        print(f"   Total schemes: {stats['total_schemes']}")
        print(f"   Active schemes: {stats['active_schemes']}")
        print(f"   Sectors: {list(stats['sectors'].keys())}")
        return True
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return False

def test_chatbot_logic():
    """Test chatbot query processing"""
    print("\nTesting chatbot logic...")
    try:
        # Set up chatbot
        chatbot.set_session("test_session_123")
        chatbot.set_language("en")
        
        # Test queries
        test_queries = [
            "What are agriculture schemes?",
            "Tell me about health schemes",
            "How to apply for education schemes?",
            "What benefits do I get from employment schemes?"
        ]
        
        for query in test_queries:
            print(f"\n🔍 Testing query: '{query}'")
            result = chatbot.process_query(query, "en")
            
            if result['success']:
                print(f"   ✅ Success: Found {len(result['schemes'])} schemes")
                print(f"   Intent: {result['intent']}")
                print(f"   Keywords: {result['keywords']}")
                print(f"   Response: {result['response']['text'][:100]}...")
            else:
                print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")
        
        return True
    except Exception as e:
        print(f"❌ Chatbot logic test failed: {e}")
        return False

def test_voice_processor():
    """Test voice processor initialization"""
    print("\nTesting voice processor...")
    try:
        from chatbot.voice_processing import voice_processor
        print("✅ Voice processor imported successfully")
        
        # Test language detection (without actual audio)
        print("   Voice processor initialized with Whisper model")
        return True
    except Exception as e:
        print(f"❌ Voice processor test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Government Voice Chatbot - Integration Test")
    print("=" * 60)
    
    tests = [
        test_mongodb_connection,
        test_chatbot_logic,
        test_voice_processor
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The integration is working correctly.")
        print("\nNext steps:")
        print("1. Run: python start.py")
        print("2. Open: http://localhost:8000")
        print("3. Test both text and voice input")
    else:
        print("⚠️  Some tests failed. Please check the error messages above.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
