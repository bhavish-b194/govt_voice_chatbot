import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'govt_voice_chatbot.settings')
import django
django.setup()
from chatbot.chatbot_logic import chatbot
import traceback

# Test the exact same call as the API
try:
    query = 'What are the agriculture schemes available?'
    language = 'en'
    session_id = 'test-session'
    
    print(f"Testing query: {query}")
    print(f"Language: {language}")
    print(f"Session ID: {session_id}")
    
    # Set chatbot session
    chatbot.set_session(session_id)
    
    # Process query
    result = chatbot.process_query(query, language)
    
    print(f"Result success: {result['success']}")
    print(f"Result keys: {result.keys()}")
    
    if result['success']:
        print(f"Schemes found: {len(result['schemes'])}")
        print(f"Response text: {result['response']['text'][:100]}...")
    else:
        print(f"Error: {result.get('error', 'No error message')}")
        
except Exception as e:
    print(f"Exception occurred: {e}")
    traceback.print_exc()
