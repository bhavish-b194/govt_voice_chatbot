#!/usr/bin/env python
"""
Quick startup script for Government Voice Chatbot
This script starts the application without dependency checks for faster startup
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    """Print application banner"""
    banner = """
    ================================================================
    |                                                              |
    |        Government Voice Chatbot - Quick Start               |
    |                                                              |
    |  * Voice-enabled chatbot for government schemes            |
    |  * Multi-language support (9 Indian languages)            |
    |  * AI-powered query processing                             |
    |  * Admin panel for scheme management                       |
    |                                                              |
    ================================================================
    """
    print(banner)

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
    
    # Setup application
    if not setup_django():
        return
    
    if not create_superuser():
        return
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()



