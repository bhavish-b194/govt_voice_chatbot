#!/usr/bin/env python
"""
Startup script for Government Voice Chatbot
This script helps initialize and start the application
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_banner():
    """Print application banner"""
    banner = """
    ================================================================
    |                                                              |
    |        Government Voice Chatbot - Startup Script            |
    |                                                              |
    |  * Voice-enabled chatbot for government schemes            |
    |  * Multi-language support (9 Indian languages)            |
    |  * AI-powered query processing                             |
    |  * Admin panel for scheme management                       |
    |                                                              |
    ================================================================
    """
    print(banner)

def check_python_version():
    """Check if Python version is compatible"""
    print("Checking Python version...")
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"OK: Python {sys.version.split()[0]} is compatible")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    print("\nChecking dependencies...")
    
    required_packages = [
        'django',
        'pymongo',
        'whisper',
        'gtts',
        'pyttsx3',
        'requests',
        'beautifulsoup4',
        'selenium'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"OK: {package}")
        except ImportError:
            print(f"ERROR: {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        
        try:
            # Install only the missing packages instead of all packages
            for package in missing_packages:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print("OK: Dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Failed to install dependencies: {e}")
            return False
    else:
        print("All dependencies are already installed - skipping installation")
    
    return True

def check_mongodb():
    """Check if MongoDB is running"""
    print("\nChecking MongoDB connection...")
    
    try:
        import pymongo
        client = pymongo.MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
        client.server_info()
        print("OK: MongoDB is running and accessible")
        return True
    except Exception as e:
        print(f"ERROR: MongoDB connection failed: {e}")
        print("   Please ensure MongoDB is installed and running")
        print("   Start MongoDB service and try again")
        return False

def setup_django():
    """Setup Django application"""
    print("\nSetting up Django application...")
    
    try:
        # Set Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'govt_voice_chatbot.settings')
        
        # Import Django
        import django
        from django.core.management import execute_from_command_line
        
        django.setup()
        
        # Run migrations
        print("Running database migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        print("OK: Database migrations completed")
        
        # Initialize sample data (if command exists)
        print("Initializing sample data...")
        try:
            execute_from_command_line(['manage.py', 'init_sample_data'])
            print("OK: Sample data initialized")
        except Exception as init_error:
            print(f"WARNING: Sample data initialization failed: {init_error}")
            print("Continuing without sample data...")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Django setup failed: {e}")
        return False

def create_superuser():
    """Create Django superuser"""
    print("\nCreating admin user...")
    
    try:
        from django.contrib.auth.models import User
        from chatbot.models import AdminUser
        
        # Check if superuser already exists
        if User.objects.filter(username='admin').exists():
            print("OK: Admin user already exists")
            return True
        
        # Create superuser
        user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        
        # Create admin user profile
        AdminUser.objects.create(
            user=user,
            role='super_admin',
            can_scrape=True,
            can_manage_schemes=True,
            can_manage_users=True
        )
        
        print("OK: Admin user created successfully")
        print("   Username: admin")
        print("   Password: admin123")
        return True
        
    except Exception as e:
        print(f"ERROR: Failed to create admin user: {e}")
        return False

def start_server():
    """Start Django development server"""
    print("\nStarting development server...")
    print("=" * 60)
    print("Government Voice Chatbot is starting...")
    print("=" * 60)
    print("\nAccess URLs:")
    print("  Main Chatbot: http://localhost:8000")
    print("  Admin Panel: http://localhost:8000/admin-panel/")
    print("  Django Admin: http://localhost:8000/admin/")
    print("\nAdmin Credentials:")
    print("  Username: admin")
    print("  Password: admin123")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])
    except KeyboardInterrupt:
        print("\n\nServer stopped. Goodbye!")
    except Exception as e:
        print(f"\nERROR: Server startup failed: {e}")

def main():
    """Main startup function"""
    print_banner()
    
    # Check prerequisites
    if not check_python_version():
        return
    
    if not check_dependencies():
        return
    
    if not check_mongodb():
        return
    
    # Setup application
    if not setup_django():
        return
    
    if not create_superuser():
        return
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()
