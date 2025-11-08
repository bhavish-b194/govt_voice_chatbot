#!/usr/bin/env python
"""
Fast startup script for Government Voice Chatbot
Just runs the Django server directly
"""

import os
import sys

def main():
    print("Starting Government Voice Chatbot...")
    print("Access URLs:")
    print("  Main Chatbot: http://localhost:8000")
    print("  Admin Panel: http://localhost:8000/admin-panel/")
    print("  Django Admin: http://localhost:8000/admin/")
    print("\nAdmin Credentials:")
    print("  Username: admin")
    print("  Password: admin123")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'govt_voice_chatbot.settings')
    
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])
    except KeyboardInterrupt:
        print("\nServer stopped. Goodbye!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()



