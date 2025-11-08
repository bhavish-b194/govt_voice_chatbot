import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'govt_voice_chatbot.settings')
import django
django.setup()
from chatbot.chatbot_logic import chatbot

# Test the exact query
query = 'What are the agriculture schemes available?'
print(f'Testing query: "{query}"')
print('=' * 50)

result = chatbot.process_query(query, 'en')
print(f'Success: {result["success"]}')
print(f'Intent: {result["intent"]}')
print(f'Schemes found: {len(result["schemes"])}')
print(f'Response: {result["response"]["text"]}')

# Debug the search process
print('\nDebugging search process:')
chatbot.set_language('en')
intent = chatbot._analyze_intent(query)
keywords = chatbot._extract_keywords(query)
entities = chatbot._extract_entities(query)

print(f'Intent: {intent}')
print(f'Keywords: {keywords}')
print(f'Entities: {entities}')

# Test direct search
schemes = chatbot._search_schemes(query, keywords, entities, intent)
print(f'Direct search result: {len(schemes)} schemes')
for scheme in schemes:
    print(f'- {scheme.title}')

# Test database directly
print('\nDirect database test:')
from chatbot.models import GovernmentScheme
agri_schemes = GovernmentScheme.objects.filter(sector='agriculture', is_active=True)
print(f'Agriculture schemes in DB: {agri_schemes.count()}')
for scheme in agri_schemes:
    print(f'- {scheme.title}')
    print(f'  Keywords: {scheme.keywords}')
    print(f'  Search Tags: {scheme.search_tags}')



