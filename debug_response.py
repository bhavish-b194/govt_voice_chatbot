import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'govt_voice_chatbot.settings')
import django
django.setup()
from chatbot.chatbot_logic import chatbot
from chatbot.models import GovernmentScheme

# Test the exact query
query = 'What are the agriculture schemes available?'
print(f'Testing query: "{query}"')
print('=' * 50)

# Set up chatbot
chatbot.set_language('en')
chatbot.set_session('test-session-123')

# Process query step by step
intent = chatbot._analyze_intent(query)
keywords = chatbot._extract_keywords(query)
entities = chatbot._extract_entities(query)
schemes = chatbot._search_schemes(query, keywords, entities, intent)

print(f'Intent: {intent}')
print(f'Keywords: {keywords}')
print(f'Entities: {entities}')
print(f'Schemes found: {len(schemes)}')

# Test response generation
response = chatbot._generate_response(query, schemes, intent, 'en')
print(f'\nGenerated response:')
print(f'Type: {type(response)}')
print(f'Text: {response["text"]}')
print(f'Confidence: {response["confidence"]}')
print(f'Scheme count: {response["scheme_count"]}')

# Test full process
print(f'\nFull process result:')
result = chatbot.process_query(query, 'en')
print(f'Success: {result["success"]}')
print(f'Response type: {type(result["response"])}')
print(f'Response text: {result["response"]["text"]}')
print(f'Schemes in result: {len(result["schemes"])}')



