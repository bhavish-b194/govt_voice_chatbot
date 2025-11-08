import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'govt_voice_chatbot.settings')
import django
django.setup()
from chatbot.chatbot_logic import chatbot
from chatbot.models import GovernmentScheme

# Test the search function step by step
query = 'What employment schemes are there?'
chatbot.set_language('en')
intent = chatbot._analyze_intent(query)
keywords = chatbot._extract_keywords(query)
entities = chatbot._extract_entities(query)

print(f'Query: {query}')
print(f'Intent: {intent}')
print(f'Keywords: {keywords}')
print(f'Entities: {entities}')

# Test the search step by step
print('\nStep-by-step search:')

# Step 1: Base query
schemes = GovernmentScheme.objects.filter(is_active=True)
print(f'1. Active schemes: {schemes.count()}')

# Step 2: Apply sector filter
if entities['sectors']:
    schemes = schemes.filter(sector__in=entities['sectors'])
    print(f'2. After sector filter ({entities["sectors"]}): {schemes.count()}')
    for scheme in schemes:
        print(f'   - {scheme.title} ({scheme.sector})')

# Step 3: Apply keyword filter
if keywords:
    from django.db.models import Q
    keyword_filters = Q()
    for keyword in keywords:
        keyword_filters |= Q(title__icontains=keyword) | Q(description__icontains=keyword) | Q(keywords__icontains=keyword)
    schemes = schemes.filter(keyword_filters)
    print(f'3. After keyword filter: {schemes.count()}')
    for scheme in schemes:
        print(f'   - {scheme.title}')

# Test the actual search function
print('\nActual search function result:')
result_schemes = chatbot._search_schemes(query, keywords, entities, intent)
print(f'Found {len(result_schemes)} schemes')
for scheme in result_schemes:
    print(f'- {scheme.title}')
