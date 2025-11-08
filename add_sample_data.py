import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'govt_voice_chatbot.settings')
import django
django.setup()
from chatbot.models import GovernmentScheme
from datetime import date

# Additional sample data for comprehensive testing
additional_schemes = [
    # Agriculture Schemes
    {
        'title': 'Pradhan Mantri Fasal Bima Yojana (PMFBY)',
        'description': 'PMFBY is a crop insurance scheme that provides comprehensive insurance coverage against crop failure, helping to stabilize the income of farmers and encourage them to adopt innovative and modern agricultural practices.',
        'short_description': 'Crop insurance scheme for farmers',
        'sector': 'agriculture',
        'ministry': 'Ministry of Agriculture and Farmers Welfare',
        'department': 'Department of Agriculture, Cooperation and Farmers Welfare',
        'government_level': 'central',
        'state': None,
        'eligibility_criteria': 'All farmers growing notified crops in notified areas',
        'benefits': 'Premium subsidy up to 90% for small and marginal farmers',
        'application_process': 'Registration through Common Service Centres (CSC) or online portal',
        'application_link': None,
        'launch_date': '2016-02-18',
        'last_date': None,
        'helpline_number': '1800-180-1551',
        'email': 'support@pmfby.gov.in',
        'website': 'https://pmfby.gov.in/',
        'source_url': 'https://pmfby.gov.in/',
        'keywords': ['crop insurance', 'agriculture', 'farmers', 'pmfby', 'fasal bima'],
        'search_tags': ['agriculture', 'central', 'crop insurance', 'farmers'],
        'language': 'en',
        'is_active': True
    },
    
    # Health Schemes
    {
        'title': 'Pradhan Mantri Matru Vandana Yojana (PMMVY)',
        'description': 'PMMVY is a maternity benefit program that provides financial assistance to pregnant and lactating mothers for their first living child.',
        'short_description': 'Maternity benefit program for pregnant women',
        'sector': 'health',
        'ministry': 'Ministry of Women and Child Development',
        'department': 'Department of Women and Child Development',
        'government_level': 'central',
        'state': None,
        'eligibility_criteria': 'Pregnant and lactating mothers above 19 years of age',
        'benefits': 'Rs.5000/- in three installments',
        'application_process': 'Registration at Anganwadi Centres or online',
        'application_link': None,
        'launch_date': '2017-01-01',
        'last_date': None,
        'helpline_number': '1800-180-1104',
        'email': 'support@wcd.nic.in',
        'website': 'https://wcd.nic.in/',
        'source_url': 'https://wcd.nic.in/',
        'keywords': ['maternity', 'health', 'women', 'pregnancy', 'pmvvy'],
        'search_tags': ['health', 'central', 'maternity', 'women welfare'],
        'language': 'en',
        'is_active': True
    },
    
    # Employment Schemes
    {
        'title': 'Pradhan Mantri Kaushal Vikas Yojana (PMKVY)',
        'description': 'PMKVY is a skill development initiative that aims to train over 10 million youth in various skills to make them employable.',
        'short_description': 'Skill development program for youth',
        'sector': 'employment',
        'ministry': 'Ministry of Skill Development and Entrepreneurship',
        'department': 'Department of Skill Development and Entrepreneurship',
        'government_level': 'central',
        'state': None,
        'eligibility_criteria': 'Indian citizens aged 15-45 years',
        'benefits': 'Free training and certification with placement assistance',
        'application_process': 'Registration through training centers or online portal',
        'application_link': None,
        'launch_date': '2015-07-15',
        'last_date': None,
        'helpline_number': '1800-123-9626',
        'email': 'support@pmkvy.gov.in',
        'website': 'https://pmkvy.gov.in/',
        'source_url': 'https://pmkvy.gov.in/',
        'keywords': ['skill development', 'employment', 'training', 'pmkvy', 'youth'],
        'search_tags': ['employment', 'central', 'skill development', 'youth'],
        'language': 'en',
        'is_active': True
    },
    
    # Education Schemes
    {
        'title': 'Pradhan Mantri Poshan Shakti Nirman (PM POSHAN)',
        'description': 'PM POSHAN is a centrally sponsored scheme that provides hot cooked meals to children studying in classes I to VIII in government and government-aided schools.',
        'short_description': 'Mid-day meal program for school children',
        'sector': 'education',
        'ministry': 'Ministry of Education',
        'department': 'Department of School Education and Literacy',
        'government_level': 'central',
        'state': None,
        'eligibility_criteria': 'Children studying in classes I to VIII in government schools',
        'benefits': 'Hot cooked meals with nutritional value',
        'application_process': 'Automatic enrollment in government schools',
        'application_link': None,
        'launch_date': '2021-09-29',
        'last_date': None,
        'helpline_number': '1800-180-5522',
        'email': 'support@education.gov.in',
        'website': 'https://education.gov.in/',
        'source_url': 'https://education.gov.in/',
        'keywords': ['education', 'mid-day meal', 'school', 'nutrition', 'children'],
        'search_tags': ['education', 'central', 'mid-day meal', 'school nutrition'],
        'language': 'en',
        'is_active': True
    },
    
    # Social Welfare Schemes
    {
        'title': 'Pradhan Mantri Ujjwala Yojana (PMUY)',
        'description': 'PMUY is a scheme to provide LPG connections to women from below poverty line (BPL) households.',
        'short_description': 'LPG connection scheme for BPL women',
        'sector': 'social_welfare',
        'ministry': 'Ministry of Petroleum and Natural Gas',
        'department': 'Department of Petroleum and Natural Gas',
        'government_level': 'central',
        'state': None,
        'eligibility_criteria': 'Women from BPL households',
        'benefits': 'Free LPG connection with first refill',
        'application_process': 'Application through LPG distributors',
        'application_link': None,
        'launch_date': '2016-05-01',
        'last_date': None,
        'helpline_number': '1800-266-6696',
        'email': 'support@petroleum.nic.in',
        'website': 'https://petroleum.nic.in/',
        'source_url': 'https://petroleum.nic.in/',
        'keywords': ['lpg', 'social welfare', 'women', 'bpl', 'ujjwala'],
        'search_tags': ['social welfare', 'central', 'lpg', 'women welfare'],
        'language': 'en',
        'is_active': True
    },
    
    # Urban Development Schemes
    {
        'title': 'Smart Cities Mission',
        'description': 'Smart Cities Mission is an urban renewal and retrofitting program to develop 100 cities across the country making them citizen friendly and sustainable.',
        'short_description': 'Urban development program for smart cities',
        'sector': 'urban_development',
        'ministry': 'Ministry of Housing and Urban Affairs',
        'department': 'Department of Housing and Urban Affairs',
        'government_level': 'central',
        'state': None,
        'eligibility_criteria': 'Cities selected through competition',
        'benefits': 'Infrastructure development and smart solutions',
        'application_process': 'City selection through competition',
        'application_link': None,
        'launch_date': '2015-06-25',
        'last_date': None,
        'helpline_number': '1800-180-5522',
        'email': 'support@smartcities.gov.in',
        'website': 'https://smartcities.gov.in/',
        'source_url': 'https://smartcities.gov.in/',
        'keywords': ['smart cities', 'urban development', 'infrastructure', 'sustainable'],
        'search_tags': ['urban development', 'central', 'smart cities', 'infrastructure'],
        'language': 'en',
        'is_active': True
    }
]

# Add the schemes to database
print("Adding additional sample schemes...")
for scheme_data in additional_schemes:
    scheme, created = GovernmentScheme.objects.get_or_create(
        title=scheme_data['title'],
        defaults=scheme_data
    )
    if created:
        print(f"[+] Added: {scheme.title}")
    else:
        print(f"[!] Already exists: {scheme.title}")

print(f"\nTotal schemes in database: {GovernmentScheme.objects.count()}")
print("Sample data addition completed!")
