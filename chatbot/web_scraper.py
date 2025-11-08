"""
Web scraping module for government portals
Fetches scheme information from various government websites
"""

import requests
from bs4 import BeautifulSoup
import time
import logging
from datetime import datetime, date
from urllib.parse import urljoin, urlparse
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import json
from typing import List, Dict, Optional
from .models import GovernmentScheme, WebScrapingLog

logger = logging.getLogger(__name__)


class GovernmentPortalScraper:
    """Scraper for government portals"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.driver = None
        self._setup_selenium()
    
    def _setup_selenium(self):
        """Setup Selenium WebDriver"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            logger.info("Selenium WebDriver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Selenium WebDriver: {e}")
            self.driver = None
    
    def __del__(self):
        """Cleanup WebDriver"""
        if self.driver:
            self.driver.quit()
    
    def scrape_india_gov_in(self) -> List[Dict]:
        """Scrape schemes from india.gov.in"""
        schemes = []
        log_entry = WebScrapingLog(
            source_url="https://www.india.gov.in/",
            source_name="India.gov.in",
            status="started",
            started_at=datetime.now()
        )
        
        try:
            # Main schemes page
            url = "https://www.india.gov.in/my-government/schemes"
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find scheme links
            scheme_links = soup.find_all('a', href=True)
            
            for link in scheme_links[:20]:  # Limit to first 20 schemes
                try:
                    href = link.get('href')
                    if not href or 'scheme' not in href.lower():
                        continue
                    
                    # Make absolute URL
                    scheme_url = urljoin(url, href)
                    
                    # Scrape individual scheme
                    scheme_data = self._scrape_scheme_page(scheme_url)
                    if scheme_data:
                        schemes.append(scheme_data)
                        time.sleep(1)  # Be respectful to the server
                        
                except Exception as e:
                    logger.error(f"Error scraping scheme link {href}: {e}")
                    continue
            
            log_entry.status = "success"
            log_entry.schemes_found = len(schemes)
            log_entry.completed_at = datetime.now()
            log_entry.duration_seconds = int((log_entry.completed_at - log_entry.started_at).total_seconds())
            
        except Exception as e:
            logger.error(f"Error scraping india.gov.in: {e}")
            log_entry.status = "failed"
            log_entry.error_message = str(e)
            log_entry.completed_at = datetime.now()
        
        finally:
            log_entry.save()
        
        return schemes
    
    def scrape_state_government_sites(self) -> List[Dict]:
        """Scrape schemes from state government websites"""
        schemes = []
        
        # List of state government portals
        state_portals = [
            {
                'name': 'Karnataka Government',
                'url': 'https://karnataka.gov.in/',
                'schemes_path': '/english/schemes'
            },
            {
                'name': 'Maharashtra Government',
                'url': 'https://www.maharashtra.gov.in/',
                'schemes_path': '/en/schemes'
            },
            {
                'name': 'Tamil Nadu Government',
                'url': 'https://www.tn.gov.in/',
                'schemes_path': '/schemes'
            }
        ]
        
        for portal in state_portals:
            try:
                portal_schemes = self._scrape_state_portal(portal)
                schemes.extend(portal_schemes)
            except Exception as e:
                logger.error(f"Error scraping {portal['name']}: {e}")
                continue
        
        return schemes
    
    def _scrape_state_portal(self, portal: Dict) -> List[Dict]:
        """Scrape schemes from a specific state portal"""
        schemes = []
        
        try:
            schemes_url = urljoin(portal['url'], portal['schemes_path'])
            response = self.session.get(schemes_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for scheme links or content
            scheme_elements = soup.find_all(['a', 'div'], class_=re.compile(r'scheme|program|yojana', re.I))
            
            for element in scheme_elements[:10]:  # Limit per state
                try:
                    if element.name == 'a' and element.get('href'):
                        scheme_url = urljoin(schemes_url, element.get('href'))
                        scheme_data = self._scrape_scheme_page(scheme_url)
                        if scheme_data:
                            scheme_data['state'] = portal['name'].replace(' Government', '')
                            schemes.append(scheme_data)
                    elif element.name == 'div':
                        # Extract text content
                        title = element.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                        if title:
                            scheme_data = {
                                'title': title.get_text().strip(),
                                'description': element.get_text().strip()[:500],
                                'source_url': schemes_url,
                                'state': portal['name'].replace(' Government', ''),
                                'government_level': 'state',
                                'ministry': 'State Government',
                                'department': 'Various Departments',
                                'sector': 'other',
                                'language': 'en'
                            }
                            schemes.append(scheme_data)
                    
                    time.sleep(0.5)
                    
                except Exception as e:
                    logger.error(f"Error processing scheme element: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error scraping state portal {portal['name']}: {e}")
        
        return schemes
    
    def _scrape_scheme_page(self, url: str) -> Optional[Dict]:
        """Scrape individual scheme page"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract scheme information
            title = self._extract_title(soup)
            description = self._extract_description(soup)
            
            if not title or not description:
                return None
            
            # Extract other details
            scheme_data = {
                'title': title,
                'description': description,
                'short_description': description[:300] + '...' if len(description) > 300 else description,
                'source_url': url,
                'government_level': 'central',
                'ministry': self._extract_ministry(soup),
                'department': self._extract_department(soup),
                'sector': self._categorize_scheme(title, description),
                'eligibility_criteria': self._extract_eligibility(soup),
                'benefits': self._extract_benefits(soup),
                'application_process': self._extract_application_process(soup),
                'launch_date': self._extract_launch_date(soup),
                'language': 'en',
                'keywords': self._extract_keywords(title, description),
                'search_tags': self._generate_search_tags(title, description),
                'is_active': True
            }
            
            return scheme_data
            
        except Exception as e:
            logger.error(f"Error scraping scheme page {url}: {e}")
            return None
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract scheme title"""
        # Try different selectors for title
        title_selectors = [
            'h1',
            '.page-title',
            '.scheme-title',
            'title',
            '.content-title'
        ]
        
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element and element.get_text().strip():
                return element.get_text().strip()
        
        return ""
    
    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract scheme description"""
        # Try different selectors for description
        desc_selectors = [
            '.scheme-description',
            '.content-description',
            '.description',
            'p',
            '.content'
        ]
        
        for selector in desc_selectors:
            elements = soup.select(selector)
            if elements:
                description = ' '.join([elem.get_text().strip() for elem in elements])
                if len(description) > 100:  # Ensure we have substantial content
                    return description
        
        return ""
    
    def _extract_ministry(self, soup: BeautifulSoup) -> str:
        """Extract responsible ministry"""
        # Look for ministry information
        ministry_keywords = ['ministry', 'department', 'ministry of']
        
        for keyword in ministry_keywords:
            elements = soup.find_all(text=re.compile(keyword, re.I))
            for element in elements:
                parent = element.parent
                if parent:
                    text = parent.get_text().strip()
                    if len(text) < 100:  # Avoid very long text
                        return text
        
        return "Government of India"
    
    def _extract_department(self, soup: BeautifulSoup) -> str:
        """Extract responsible department"""
        # Similar to ministry extraction
        dept_keywords = ['department', 'division', 'board', 'commission']
        
        for keyword in dept_keywords:
            elements = soup.find_all(text=re.compile(keyword, re.I))
            for element in elements:
                parent = element.parent
                if parent:
                    text = parent.get_text().strip()
                    if len(text) < 100:
                        return text
        
        return "Various Departments"
    
    def _categorize_scheme(self, title: str, description: str) -> str:
        """Categorize scheme into sectors based on keywords"""
        text = (title + ' ' + description).lower()
        
        sector_keywords = {
            'agriculture': ['agriculture', 'farmer', 'crop', 'irrigation', 'soil', 'farming', 'kisan'],
            'health': ['health', 'medical', 'hospital', 'doctor', 'medicine', 'treatment', 'ayushman'],
            'education': ['education', 'school', 'college', 'student', 'scholarship', 'learning', 'skill'],
            'employment': ['employment', 'job', 'work', 'skill', 'training', 'employment', 'rogar'],
            'social_welfare': ['welfare', 'pension', 'widow', 'disabled', 'senior', 'social'],
            'rural_development': ['rural', 'village', 'gram', 'panchayat', 'rural development'],
            'women_empowerment': ['women', 'girl', 'female', 'empowerment', 'beti', 'mahila'],
            'youth_development': ['youth', 'young', 'student', 'youth development']
        }
        
        for sector, keywords in sector_keywords.items():
            if any(keyword in text for keyword in keywords):
                return sector
        
        return 'other'
    
    def _extract_eligibility(self, soup: BeautifulSoup) -> str:
        """Extract eligibility criteria"""
        eligibility_keywords = ['eligibility', 'eligible', 'criteria', 'qualification', 'who can apply']
        
        for keyword in eligibility_keywords:
            elements = soup.find_all(text=re.compile(keyword, re.I))
            for element in elements:
                parent = element.parent
                if parent:
                    text = parent.get_text().strip()
                    if len(text) > 50 and len(text) < 1000:
                        return text
        
        return "Please check official website for eligibility criteria"
    
    def _extract_benefits(self, soup: BeautifulSoup) -> str:
        """Extract benefits information"""
        benefit_keywords = ['benefit', 'advantage', 'assistance', 'support', 'help', 'aid']
        
        for keyword in benefit_keywords:
            elements = soup.find_all(text=re.compile(keyword, re.I))
            for element in elements:
                parent = element.parent
                if parent:
                    text = parent.get_text().strip()
                    if len(text) > 50 and len(text) < 1000:
                        return text
        
        return "Please check official website for benefits details"
    
    def _extract_application_process(self, soup: BeautifulSoup) -> str:
        """Extract application process"""
        process_keywords = ['apply', 'application', 'process', 'procedure', 'how to apply']
        
        for keyword in process_keywords:
            elements = soup.find_all(text=re.compile(keyword, re.I))
            for element in elements:
                parent = element.parent
                if parent:
                    text = parent.get_text().strip()
                    if len(text) > 50 and len(text) < 1000:
                        return text
        
        return "Please visit official website for application process"
    
    def _extract_launch_date(self, soup: BeautifulSoup) -> date:
        """Extract launch date"""
        # Look for date patterns
        date_patterns = [
            r'\d{1,2}[/-]\d{1,2}[/-]\d{4}',
            r'\d{4}[/-]\d{1,2}[/-]\d{1,2}',
            r'\d{1,2}\s+\w+\s+\d{4}'
        ]
        
        for pattern in date_patterns:
            elements = soup.find_all(text=re.compile(pattern))
            for element in elements:
                try:
                    # Try to parse the date
                    date_str = re.search(pattern, element).group()
                    # Simple date parsing (can be improved)
                    return date.today()  # Placeholder
                except:
                    continue
        
        return date.today()
    
    def _extract_keywords(self, title: str, description: str) -> List[str]:
        """Extract keywords from title and description"""
        text = (title + ' ' + description).lower()
        
        # Common keywords to extract
        keywords = []
        
        # Government scheme related keywords
        scheme_keywords = ['scheme', 'program', 'yojana', 'initiative', 'policy', 'plan']
        for keyword in scheme_keywords:
            if keyword in text:
                keywords.append(keyword)
        
        # Sector keywords
        sector_keywords = ['agriculture', 'health', 'education', 'employment', 'welfare', 'development']
        for keyword in sector_keywords:
            if keyword in text:
                keywords.append(keyword)
        
        return keywords[:10]  # Limit to 10 keywords
    
    def _generate_search_tags(self, title: str, description: str) -> List[str]:
        """Generate search tags for better searchability"""
        text = (title + ' ' + description).lower()
        
        tags = []
        
        # Add sector tags
        if any(word in text for word in ['farmer', 'agriculture', 'crop']):
            tags.append('agriculture')
        if any(word in text for word in ['health', 'medical', 'hospital']):
            tags.append('health')
        if any(word in text for word in ['education', 'school', 'student']):
            tags.append('education')
        if any(word in text for word in ['job', 'employment', 'work']):
            tags.append('employment')
        
        # Add government level tags
        if 'central' in text or 'national' in text:
            tags.append('central')
        if 'state' in text:
            tags.append('state')
        
        return tags
    
    def save_schemes_to_database(self, schemes: List[Dict]) -> Dict:
        """Save scraped schemes to database"""
        added_count = 0
        updated_count = 0
        
        for scheme_data in schemes:
            try:
                # Check if scheme already exists
                existing_scheme = GovernmentScheme.objects.filter(
                    title__iexact=scheme_data['title'],
                    source_url=scheme_data['source_url']
                ).first()
                
                if existing_scheme:
                    # Update existing scheme
                    for key, value in scheme_data.items():
                        if hasattr(existing_scheme, key):
                            setattr(existing_scheme, key, value)
                    existing_scheme.save()
                    updated_count += 1
                else:
                    # Create new scheme
                    GovernmentScheme.objects.create(**scheme_data)
                    added_count += 1
                    
            except Exception as e:
                logger.error(f"Error saving scheme {scheme_data.get('title', 'Unknown')}: {e}")
                continue
        
        return {
            'added': added_count,
            'updated': updated_count,
            'total_processed': len(schemes)
        }
    
    def run_full_scraping(self) -> Dict:
        """Run full scraping process"""
        logger.info("Starting full scraping process")
        
        all_schemes = []
        
        # Scrape central government schemes
        try:
            central_schemes = self.scrape_india_gov_in()
            all_schemes.extend(central_schemes)
            logger.info(f"Scraped {len(central_schemes)} central government schemes")
        except Exception as e:
            logger.error(f"Error scraping central schemes: {e}")
        
        # Scrape state government schemes
        try:
            state_schemes = self.scrape_state_government_sites()
            all_schemes.extend(state_schemes)
            logger.info(f"Scraped {len(state_schemes)} state government schemes")
        except Exception as e:
            logger.error(f"Error scraping state schemes: {e}")
        
        # Save to database
        save_result = self.save_schemes_to_database(all_schemes)
        
        logger.info(f"Scraping completed. Added: {save_result['added']}, Updated: {save_result['updated']}")
        
        return {
            'total_scraped': len(all_schemes),
            'added_to_db': save_result['added'],
            'updated_in_db': save_result['updated'],
            'errors': len(all_schemes) - save_result['total_processed']
        }


# Global scraper instance
scraper = GovernmentPortalScraper()
