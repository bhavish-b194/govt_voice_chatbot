import requests
import json

# Test multiple queries to ensure MongoDB is working
queries = [
    'What are the agriculture schemes available?',
    'Tell me about health schemes', 
    'What employment schemes are there?',
    'Show me education schemes',
    'What social welfare schemes exist?',
    'Tell me about urban development schemes'
]

print('Testing all sector queries:')
print('=' * 50)

for query in queries:
    try:
        response = requests.post('http://localhost:8000/api/chat/text/', json={'query': query, 'language': 'en'})
        if response.status_code == 200:
            data = response.json()
            print(f'Query: {query}')
            print(f'  Success: {data["success"]}')
            print(f'  Schemes: {len(data["schemes"])}')
            if data['schemes']:
                print(f'  Sample: {data["schemes"][0]["title"]}')
            print()
        else:
            print(f'Error for {query}: {response.status_code}')
    except Exception as e:
        print(f'Exception for {query}: {e}')
