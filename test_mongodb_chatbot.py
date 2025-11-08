import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'govt_voice_chatbot.settings')
import django
django.setup()
from chatbot.chatbot_logic import chatbot

# Test comprehensive queries with MongoDB
test_queries = [
    'What are the agriculture schemes available?',
    'Tell me about health schemes',
    'What employment schemes are there?',
    'Show me education schemes',
    'What social welfare schemes exist?',
    'Tell me about urban development schemes',
    'What government schemes are available?',
    'Tell me about loan schemes',
    'What schemes are for farmers?',
    'What schemes are for women?'
]

print("Testing Chatbot with MongoDB:")
print("=" * 50)

for query in test_queries:
    print(f'\nQuery: "{query}"')
    result = chatbot.process_query(query, 'en')
    print(f'Success: {result["success"]}')
    print(f'Schemes found: {len(result["schemes"])}')
    if result["schemes"]:
        for scheme in result["schemes"][:2]:  # Show first 2 schemes
            print(f'  - {scheme["title"]} ({scheme["sector"]})')
    else:
        print('  No schemes found')
    print(f'Response: {result["response"]["text"][:100]}...')
