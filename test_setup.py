#!/usr/bin/env python
"""
Test script to verify the Government Voice Chatbot setup
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'govt_voice_chatbot.settings')
django.setup()

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import whisper
        print("✅ OpenAI Whisper imported successfully")
    except ImportError as e:
        print(f"❌ OpenAI Whisper import failed: {e}")
    
    try:
        import pyttsx3
        print("✅ pyttsx3 imported successfully")
    except ImportError as e:
        print(f"❌ pyttsx3 import failed: {e}")
    
    try:
        from gtts import gTTS
        print("✅ gTTS imported successfully")
    except ImportError as e:
        print(f"❌ gTTS import failed: {e}")
    
    try:
        import pymongo
        print("✅ PyMongo imported successfully")
    except ImportError as e:
        print(f"❌ PyMongo import failed: {e}")
    
    try:
        from selenium import webdriver
        print("✅ Selenium imported successfully")
    except ImportError as e:
        print(f"❌ Selenium import failed: {e}")
    
    try:
        from bs4 import BeautifulSoup
        print("✅ BeautifulSoup imported successfully")
    except ImportError as e:
        print(f"❌ BeautifulSoup import failed: {e}")

def test_django_setup():
    """Test Django setup"""
    print("\nTesting Django setup...")
    
    try:
        from django.conf import settings
        print("✅ Django settings loaded successfully")
        print(f"   - DEBUG: {settings.DEBUG}")
        print(f"   - Database: {settings.DATABASES['default']['ENGINE']}")
    except Exception as e:
        print(f"❌ Django setup failed: {e}")

def test_models():
    """Test model imports"""
    print("\nTesting model imports...")
    
    try:
        from chatbot.models import GovernmentScheme, ChatSession, ChatMessage
        print("✅ Chatbot models imported successfully")
    except Exception as e:
        print(f"❌ Chatbot models import failed: {e}")
    
    try:
        from admin_panel.models import AdminUser
        print("✅ Admin panel models imported successfully")
    except Exception as e:
        print(f"❌ Admin panel models import failed: {e}")

def test_voice_processing():
    """Test voice processing modules"""
    print("\nTesting voice processing...")
    
    try:
        from chatbot.voice_processing import VoiceProcessor
        print("✅ Voice processing module imported successfully")
        
        # Test voice processor initialization
        processor = VoiceProcessor()
        print("✅ Voice processor initialized successfully")
    except Exception as e:
        print(f"❌ Voice processing test failed: {e}")

def test_chatbot_logic():
    """Test chatbot logic"""
    print("\nTesting chatbot logic...")
    
    try:
        from chatbot.chatbot_logic import GovernmentChatbot
        print("✅ Chatbot logic imported successfully")
        
        # Test chatbot initialization
        chatbot = GovernmentChatbot()
        print("✅ Chatbot initialized successfully")
    except Exception as e:
        print(f"❌ Chatbot logic test failed: {e}")

def test_web_scraper():
    """Test web scraper"""
    print("\nTesting web scraper...")
    
    try:
        from chatbot.web_scraper import GovernmentPortalScraper
        print("✅ Web scraper imported successfully")
        
        # Test scraper initialization
        scraper = GovernmentPortalScraper()
        print("✅ Web scraper initialized successfully")
    except Exception as e:
        print(f"❌ Web scraper test failed: {e}")

def test_database_connection():
    """Test database connection"""
    print("\nTesting database connection...")
    
    try:
        from django.db import connection
        connection.ensure_connection()
        print("✅ Database connection successful")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("   Make sure MongoDB is running and accessible")

def main():
    """Run all tests"""
    print("Government Voice Chatbot - Setup Test")
    print("=" * 50)
    
    test_imports()
    test_django_setup()
    test_models()
    test_voice_processing()
    test_chatbot_logic()
    test_web_scraper()
    test_database_connection()
    
    print("\n" + "=" * 50)
    print("Setup test completed!")
    print("\nNext steps:")
    print("1. Install missing dependencies if any")
    print("2. Start MongoDB service")
    print("3. Run: python manage.py migrate")
    print("4. Run: python manage.py runserver")
    print("5. Open http://localhost:8000 in your browser")

if __name__ == "__main__":
    main()
