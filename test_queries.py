import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'govt_voice_chatbot.settings')
import django
django.setup()
from chatbot.chatbot_logic import chatbot

# Test different queries
queries = [
    'What are the agriculture schemes available?',
    'Tell me about health schemes',
    'What employment schemes are there?',
    'Show me housing schemes',
    'What government schemes are available?'
]

for query in queries:
    print(f'Testing: "{query}"')
    result = chatbot.process_query(query, 'en')
    print(f'  Success: {result["success"]}')
    print(f'  Schemes found: {len(result["schemes"])}')
    print(f'  Response: {result["response"]["text"][:100]}...')
    print()



