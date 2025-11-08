import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'govt_voice_chatbot.settings')
import django
django.setup()

# Test MongoDB adapter import
try:
    from mongodb_adapter import MongoDBAdapter
    print("MongoDB adapter import successful")
    
    adapter = MongoDBAdapter()
    schemes = adapter.search_schemes(
        "What are the agriculture schemes available?",
        ["agriculture", "schemes"],
        {"sectors": ["agriculture"]},
        "sector_specific"
    )
    print(f"Found {len(schemes)} schemes")
    
except Exception as e:
    print(f"MongoDB adapter error: {e}")
    import traceback
    traceback.print_exc()
