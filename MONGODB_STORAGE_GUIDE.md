# 📊 MongoDB Storage Guide - Kannada Government Schemes

## 🎯 **Exact Storage Location**

### **Database Details:**
- **Host**: `localhost`
- **Port**: `27017`
- **Database Name**: `Govt_schemes`
- **Collection Name**: `government_schemes`
- **Total Documents**: 35 schemes
- **Kannada Schemes**: 5 schemes

### **Full MongoDB Path:**
```
mongodb://localhost:27017/Govt_schemes/government_schemes
```

---

## 🇮🇳 **Kannada Schemes Stored in MongoDB**

### **1. ಕೃಷಿ ಸಿಂಚನ ಯೋಜನೆ (Agriculture Irrigation Scheme)**
- **Document ID**: `690cca2c54d3507d9e2594ed`
- **Sector**: `agriculture`
- **State**: `Karnataka`
- **Ministry**: `ಕೃಷಿ ಸಚಿವಾಲಯ, ಕರ್ನಾಟಕ`

### **2. ಆರೋಗ್ಯ ಶ್ರೀ ಯೋಜನೆ (Health Care Scheme)**
- **Document ID**: `690cca2c54d3507d9e2594ee`
- **Sector**: `health`
- **State**: `Karnataka`
- **Ministry**: `ಆರೋಗ್ಯ ಮತ್ತು ಕುಟುಂಬ ಕಲ್ಯಾಣ ಸಚಿವಾಲಯ, ಕರ್ನಾಟಕ`

### **3. ವಿದ್ಯಾಸಿರಿ ವಿದ್ಯಾರ್ಥಿವೇತನ (Education Scholarship)**
- **Document ID**: `690cca2c54d3507d9e2594ef`
- **Sector**: `education`
- **State**: `Karnataka`
- **Ministry**: `ಪ್ರಾಥಮಿಕ ಮತ್ತು ಮಾಧ್ಯಮಿಕ ಶಿಕ್ಷಣ ಸಚಿವಾಲಯ, ಕರ್ನಾಟಕ`

### **4. ಭಾಗ್ಯಲಕ್ಷ್ಮಿ ಯೋಜನೆ (Girl Child Welfare Scheme)**
- **Document ID**: `690cca2c54d3507d9e2594f0`
- **Sector**: `women_empowerment`
- **State**: `Karnataka`
- **Ministry**: `ಮಹಿಳಾ ಮತ್ತು ಮಕ್ಕಳ ಅಭಿವೃದ್ಧಿ ಸಚಿವಾಲಯ, ಕರ್ನಾಟಕ`

### **5. ಇಂದಿರಾ ಆವಾಸ್ ಯೋಜನೆ (Housing Scheme)**
- **Document ID**: `690cca2c54d3507d9e2594f1`
- **Sector**: `housing`
- **State**: `Karnataka`
- **Ministry**: `ಗ್ರಾಮೀಣ ಅಭಿವೃದ್ಧಿ ಮತ್ತು ಪಂಚಾಯತ್ ರಾಜ್ ಸಚಿವಾಲಯ, ಕರ್ನಾಟಕ`

---

## 💻 **How to Access Kannada Schemes Data**

### **Method 1: Python with PyMongo**
```python
import pymongo

# Connect to MongoDB
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['Govt_schemes']
schemes = db['government_schemes']

# Get all Kannada schemes
kannada_schemes = list(schemes.find({'state': 'Karnataka'}))

# Get specific sector schemes
agriculture_schemes = schemes.find({'sector': 'agriculture', 'state': 'Karnataka'})
health_schemes = schemes.find({'sector': 'health', 'state': 'Karnataka'})
education_schemes = schemes.find({'sector': 'education', 'state': 'Karnataka'})
```

### **Method 2: MongoDB Shell Commands**
```bash
# Connect to MongoDB
mongo

# Use the database
use Govt_schemes

# Find all Kannada schemes
db.government_schemes.find({"state": "Karnataka"})

# Find by sector
db.government_schemes.find({"sector": "agriculture", "state": "Karnataka"})

# Count Kannada schemes
db.government_schemes.count({"state": "Karnataka"})
```

### **Method 3: MongoDB Compass (GUI)**
1. **Connect to**: `mongodb://localhost:27017`
2. **Navigate to**: `Govt_schemes` database
3. **Open**: `government_schemes` collection
4. **Filter by**: `{"state": "Karnataka"}`

---

## 📋 **Document Structure in MongoDB**

Each Kannada scheme document contains these fields:

```json
{
  "_id": "ObjectId",
  "title": "ಕೃಷಿ ಸಿಂಚನ ಯೋಜನೆ (Krishi Sinchana Yojane)",
  "description": "ಕರ್ನಾಟಕ ಸರ್ಕಾರದ ಕೃಷಿ ಸಿಂಚನ ಯೋಜನೆ...",
  "short_description": "ರೈತರಿಗೆ ಉಚಿತ ಸಿಂಚನ ಸೌಲಭ್ಯಗಳು...",
  "sector": "agriculture",
  "ministry": "ಕೃಷಿ ಸಚಿವಾಲಯ, ಕರ್ನಾಟಕ",
  "department": "ಕೃಷಿ ಇಲಾಖೆ",
  "government_level": "state",
  "state": "Karnataka",
  "eligibility_criteria": "ಕರ್ನಾಟಕದ ಎಲ್ಲಾ ರೈತರು...",
  "benefits": "ಬೋರ್‌ವೆಲ್‌ಗೆ ₹1,00,000 ವರೆಗೆ...",
  "application_process": "ಹತ್ತಿರದ ಕೃಷಿ ಕಚೇರಿಯಲ್ಲಿ...",
  "launch_date": "2020-01-01",
  "helpline_number": "080-22212448",
  "website": "https://agriculture.karnataka.gov.in/",
  "source_url": "https://agriculture.karnataka.gov.in/",
  "keywords": ["ಕೃಷಿ", "ಸಿಂಚನ", "ರೈತರು"],
  "search_tags": ["agriculture", "state", "irrigation"],
  "is_active": true,
  "created_at": "2025-11-06T16:18:00.000Z",
  "updated_at": "2025-11-06T16:18:00.000Z"
}
```

---

## 🔍 **Search Queries for Kannada Data**

### **Find by Kannada Keywords**
```python
# Search by Kannada text in title
schemes.find({"title": {"$regex": "ಕೃಷಿ", "$options": "i"}})

# Search by Kannada keywords
schemes.find({"keywords": {"$in": ["ಆರೋಗ್ಯ", "ಚಿಕಿತ್ಸೆ"]}})

# Search by ministry in Kannada
schemes.find({"ministry": {"$regex": "ಸಚಿವಾಲಯ", "$options": "i"}})
```

### **Advanced Filtering**
```python
# Get schemes by multiple criteria
schemes.find({
    "state": "Karnataka",
    "sector": "agriculture",
    "is_active": True
})

# Get schemes with specific benefits
schemes.find({
    "state": "Karnataka",
    "benefits": {"$regex": "₹", "$options": "i"}
})
```

---

## 🛠️ **How the Application Accesses This Data**

### **1. Django Models (Optional)**
The data can be accessed through Django models in `chatbot/models.py`:
```python
from chatbot.models import GovernmentScheme

# Get Kannada schemes through Django
kannada_schemes = GovernmentScheme.objects.filter(state='Karnataka')
```

### **2. MongoDB Adapter**
The application uses `mongodb_adapter.py` to access data:
```python
from mongodb_adapter import MongoDBAdapter

adapter = MongoDBAdapter()
kannada_schemes = adapter.search_schemes(
    query="ಕೃಷಿ ಯೋಜನೆ",
    keywords=["ಕೃಷಿ"],
    entities={"state": "Karnataka"},
    intent="search_scheme"
)
```

### **3. API Endpoints**
The schemes are accessible through REST API:
- **GET** `/api/schemes/search/` - Search all schemes
- **POST** `/api/chat/advanced-search/` - Advanced search with filters
- **GET** `/api/schemes/sectors/` - Get schemes by sector

---

## 📊 **Database Statistics**

### **Storage Information:**
- **Database Size**: ~2-5 MB (estimated)
- **Collection Size**: 35 documents
- **Kannada Documents**: 5 documents
- **Index Fields**: sector, state, is_active
- **Text Encoding**: UTF-8 (supports Kannada Unicode)

### **Performance:**
- **Query Speed**: Fast (indexed fields)
- **Search Capability**: Full-text search in Kannada
- **Scalability**: Can handle thousands of schemes

---

## 🚀 **Backup and Maintenance**

### **Backup Kannada Data**
```bash
# Export Kannada schemes only
mongoexport --db=Govt_schemes --collection=government_schemes --query='{"state":"Karnataka"}' --out=kannada_schemes.json

# Import backup
mongoimport --db=Govt_schemes --collection=government_schemes --file=kannada_schemes.json
```

### **Update Kannada Schemes**
```python
# Update a specific scheme
schemes.update_one(
    {"title": "ಕೃಷಿ ಸಿಂಚನ ಯೋಜನೆ (Krishi Sinchana Yojane)"},
    {"$set": {"benefits": "Updated benefits in Kannada"}}
)
```

---

## 🎯 **Summary**

✅ **Location**: `mongodb://localhost:27017/Govt_schemes/government_schemes`
✅ **Documents**: 5 Kannada schemes with proper Unicode
✅ **Searchable**: Full Kannada text search capability
✅ **Accessible**: Through Python, MongoDB shell, or GUI tools
✅ **Integrated**: Works with Django application and REST APIs
✅ **Maintainable**: Easy to backup, update, and scale

**Your Kannada government schemes are securely stored in MongoDB and fully accessible through multiple methods!** 🇮🇳✨
