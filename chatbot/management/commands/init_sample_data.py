"""
Management command to initialize sample government schemes data
"""

from django.core.management.base import BaseCommand
from chatbot.models import GovernmentScheme
from datetime import date, datetime
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Initialize sample government schemes data'

    def handle(self, *args, **options):
        self.stdout.write('Initializing sample government schemes data...')
        
        sample_schemes = [
            {
                'title': 'Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)',
                'description': 'PM-KISAN is a Central Sector Scheme with 100% funding from Government of India. Under the scheme, income support of Rs.6000/- per year is provided to all farmer families across the country in three equal installments of Rs.2000/- each every four months.',
                'short_description': 'Income support of Rs.6000/- per year to all farmer families',
                'sector': 'agriculture',
                'ministry': 'Ministry of Agriculture and Farmers Welfare',
                'department': 'Department of Agriculture, Cooperation and Farmers Welfare',
                'government_level': 'central',
                'eligibility_criteria': 'All landholding farmer families with cultivable land in their names',
                'benefits': 'Rs.6000/- per year in three equal installments of Rs.2000/- each',
                'application_process': 'Registration through Common Service Centres (CSC) or online portal',
                'launch_date': date(2019, 2, 1),
                'language': 'en',
                'keywords': ['farmer', 'agriculture', 'income support', 'pm-kisan'],
                'search_tags': ['agriculture', 'central', 'farmer welfare'],
                'source_url': 'https://pmkisan.gov.in/',
                'is_active': True
            },
            {
                'title': 'Ayushman Bharat Pradhan Mantri Jan Arogya Yojana (AB-PMJAY)',
                'description': 'AB-PMJAY is the largest health assurance scheme in the world which aims at providing a health cover of Rs. 5 lakhs per family per year for secondary and tertiary care hospitalization to over 10.74 crores poor and vulnerable families.',
                'short_description': 'Health cover of Rs. 5 lakhs per family per year for hospitalization',
                'sector': 'health',
                'ministry': 'Ministry of Health and Family Welfare',
                'department': 'Department of Health and Family Welfare',
                'government_level': 'central',
                'eligibility_criteria': 'Families identified as per SECC database, having deprivation criteria',
                'benefits': 'Health cover of Rs. 5 lakhs per family per year for secondary and tertiary care hospitalization',
                'application_process': 'Eligible families can avail services at empaneled hospitals',
                'launch_date': date(2018, 9, 23),
                'language': 'en',
                'keywords': ['health', 'medical', 'hospitalization', 'ayushman bharat'],
                'search_tags': ['health', 'central', 'medical insurance'],
                'source_url': 'https://pmjay.gov.in/',
                'is_active': True
            },
            {
                'title': 'Pradhan Mantri Jan Dhan Yojana (PMJDY)',
                'description': 'PMJDY is a National Mission for Financial Inclusion to ensure access to financial services, namely, Banking/ Savings & Deposit Accounts, Remittance, Credit, Insurance, Pension in an affordable manner.',
                'short_description': 'Financial inclusion mission to provide banking services to all',
                'sector': 'social_welfare',
                'ministry': 'Ministry of Finance',
                'department': 'Department of Financial Services',
                'government_level': 'central',
                'eligibility_criteria': 'All unbanked households in the country',
                'benefits': 'Zero balance savings account, RuPay debit card, accident insurance cover of Rs.1 lakh',
                'application_process': 'Visit any bank branch or Business Correspondent outlet',
                'launch_date': date(2014, 8, 28),
                'language': 'en',
                'keywords': ['banking', 'financial inclusion', 'jan dhan', 'savings account'],
                'search_tags': ['social welfare', 'central', 'banking'],
                'source_url': 'https://pmjdy.gov.in/',
                'is_active': True
            },
            {
                'title': 'Pradhan Mantri Mudra Yojana (PMMY)',
                'description': 'PMMY is a scheme launched by the Hon\'ble Prime Minister on April 8, 2015 for providing loans up to 10 lakh to the non-corporate, non-farm small/micro enterprises.',
                'short_description': 'Loans up to 10 lakh for small/micro enterprises',
                'sector': 'employment',
                'ministry': 'Ministry of Finance',
                'department': 'Department of Financial Services',
                'government_level': 'central',
                'eligibility_criteria': 'Non-corporate, non-farm small/micro enterprises',
                'benefits': 'Loans up to Rs.10 lakh under three categories: Shishu (up to Rs.50,000), Kishore (Rs.50,000 to Rs.5 lakh), Tarun (Rs.5 lakh to Rs.10 lakh)',
                'application_process': 'Apply through any of the lending institutions like Banks, NBFCs, MFIs',
                'launch_date': date(2015, 4, 8),
                'language': 'en',
                'keywords': ['loan', 'mudra', 'small business', 'micro enterprise'],
                'search_tags': ['employment', 'central', 'loan'],
                'source_url': 'https://mudra.org.in/',
                'is_active': True
            },
            {
                'title': 'Pradhan Mantri Awas Yojana (PMAY)',
                'description': 'PMAY is a flagship mission of Government of India implemented by Ministry of Housing and Urban Affairs (MoHUA), was launched on 25th June 2015. The Mission addresses urban housing shortage among the EWS/LIG and MIG categories including the slum dwellers.',
                'short_description': 'Housing for all by 2022 - affordable housing scheme',
                'sector': 'urban_development',
                'ministry': 'Ministry of Housing and Urban Affairs',
                'department': 'Ministry of Housing and Urban Affairs',
                'government_level': 'central',
                'eligibility_criteria': 'EWS/LIG/MIG families as per income criteria',
                'benefits': 'Central assistance of Rs.1.5 lakh to Rs.2.67 lakh for construction of house',
                'application_process': 'Apply online through PMAY portal or visit concerned authority',
                'launch_date': date(2015, 6, 25),
                'language': 'en',
                'keywords': ['housing', 'pmay', 'affordable housing', 'urban development'],
                'search_tags': ['urban development', 'central', 'housing'],
                'source_url': 'https://pmaymis.gov.in/',
                'is_active': True
            }
        ]
        
        created_count = 0
        updated_count = 0
        
        for scheme_data in sample_schemes:
            try:
                scheme, created = GovernmentScheme.objects.get_or_create(
                    title=scheme_data['title'],
                    defaults=scheme_data
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(f'Created: {scheme.title}')
                else:
                    # Update existing scheme
                    for key, value in scheme_data.items():
                        setattr(scheme, key, value)
                    scheme.save()
                    updated_count += 1
                    self.stdout.write(f'Updated: {scheme.title}')
                    
            except Exception as e:
                self.stderr.write(f'Error processing {scheme_data["title"]}: {e}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully processed {len(sample_schemes)} schemes. '
                f'Created: {created_count}, Updated: {updated_count}'
            )
        )
        
        # Display summary
        total_schemes = GovernmentScheme.objects.count()
        active_schemes = GovernmentScheme.objects.filter(is_active=True).count()
        
        self.stdout.write(f'Total schemes in database: {total_schemes}')
        self.stdout.write(f'Active schemes: {active_schemes}')
        
        self.stdout.write(
            self.style.SUCCESS('Sample data initialization completed successfully!')
        )
