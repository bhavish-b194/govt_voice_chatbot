import pymongo

# Connect to MongoDB
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['govt_schemes']
schemes = db['government_schemes']

print(f'Total schemes in MongoDB: {schemes.count_documents({})}')
print(f'Active schemes: {schemes.count_documents({"is_active": True})}')

sectors = schemes.distinct('sector')
print(f'Sectors: {sectors}')

for sector in sectors:
    count = schemes.count_documents({'sector': sector, 'is_active': True})
    print(f'  {sector}: {count} schemes')

# Test a sample query
print('\nSample agriculture schemes:')
agri_schemes = schemes.find({'sector': 'agriculture', 'is_active': True}).limit(3)
for scheme in agri_schemes:
    print(f'  - {scheme["title"]}')
