import requests

try:
    response = requests.post('http://localhost:8000/api/chat/text/', json={'query': 'What are the agriculture schemes available?', 'language': 'en'})
    print('API Status:', response.status_code)
    if response.status_code == 200:
        data = response.json()
        print('Success:', data['success'])
        print('Schemes found:', len(data['schemes']))
        print('Response preview:', data['response']['text'][:150])
        print('Sample schemes:')
        for scheme in data['schemes'][:3]:
            print(f'  - {scheme["title"]} ({scheme["sector"]})')
    else:
        print('Error:', response.text)
except Exception as e:
    print('Connection error:', e)
