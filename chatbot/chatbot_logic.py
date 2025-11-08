"""
Chatbot logic for processing user queries and returning relevant scheme information
Supports multiple languages and intelligent query processing
"""

import re
import logging
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from .models import GovernmentScheme, ChatSession, ChatMessage
from .voice_processing import voice_processor
import json

logger = logging.getLogger(__name__)


class GovernmentChatbot:
    """Main chatbot class for processing government scheme queries"""
    
    def __init__(self):
        self.language = 'en'
        self.session_id = None
        self.session = None
    
    def set_language(self, language: str):
        """Set the language for responses"""
        self.language = language
    
    def set_session(self, session_id: str):
        """Set the current chat session"""
        self.session_id = session_id
        try:
            self.session = ChatSession.objects.get(session_id=session_id)
        except ChatSession.DoesNotExist:
            self.session = ChatSession.objects.create(
                session_id=session_id,
                language=self.language
            )
    
    def process_query(self, query: str, language: str = 'en') -> Dict:
        """
        Process user query and return relevant scheme information
        Args:
            query: User's query text
            language: Language of the query
        Returns:
            dict with response information
        """
        try:
            self.set_language(language)
            
            # Log user message
            if self.session:
                ChatMessage.objects.create(
                    session=self.session,
                    message_type='user',
                    text_content=query,
                    language=language
                )
            
            # Analyze query intent
            intent = self._analyze_intent(query)
            
            # Extract keywords and entities
            keywords = self._extract_keywords(query)
            entities = self._extract_entities(query)
            
            # Search for relevant schemes
            relevant_schemes = self._search_schemes(query, keywords, entities, intent)
            
            # Generate response
            response = self._generate_response(query, relevant_schemes, intent, language)
            
            # Log bot response
            if self.session:
                ChatMessage.objects.create(
                    session=self.session,
                    message_type='bot',
                    text_content=response['text'],
                    language=language,
                    related_schemes=[scheme.get('_id', '') for scheme in relevant_schemes[:3]],
                    confidence_score=response.get('confidence', 0.8)
                )
            
            return {
                'success': True,
                'response': response,
                'schemes': [self._format_scheme(scheme) for scheme in relevant_schemes[:5]],
                'intent': intent,
                'keywords': keywords,
                'language': language
            }
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                'success': False,
                'error': str(e),
                'response': {
                    'text': self._get_error_response(language),
                    'confidence': 0.0,
                    'intent': 'error',
                    'scheme_count': 0
                }
            }
    
    def process_voice_query(self, audio_file_path: str) -> Dict:
        """
        Process voice query: convert speech to text and process
        Args:
            audio_file_path: Path to the audio file
        Returns:
            dict with response and audio
        """
        try:
            # Convert speech to text using voice processor
            stt_result = voice_processor.process_voice_input(audio_file_path)
            
            if not stt_result['success']:
                return {
                    'success': False,
                    'error': stt_result['error'],
                    'text_response': 'Voice processing failed. Please try again or use text input.',
                    'audio_response': None,
                    'language': 'en',
                    'schemes': [],
                    'confidence': 0.0
                }
            
            # Process the text query using our chatbot logic
            query_result = self.process_query(
                stt_result['text'], 
                stt_result['language']
            )
            
            if not query_result['success']:
                return {
                    'success': False,
                    'error': query_result.get('error', 'Query processing failed'),
                    'text_response': query_result['response']['text'],
                    'audio_response': None,
                    'language': stt_result['language'],
                    'schemes': [],
                    'confidence': 0.0
                }
            
            # Generate voice response
            try:
                voice_result = voice_processor.generate_voice_response(
                    query_result['response']['text'],
                    query_result['language']
                )
                audio_response = voice_result.get('audio_data') if voice_result.get('success') else None
            except Exception as e:
                logger.warning(f"Voice response generation failed: {e}")
                audio_response = None
            
            return {
                'success': True,
                'text_response': query_result['response']['text'],
                'audio_response': audio_response,
                'language': query_result['language'],
                'schemes': query_result['schemes'],
                'confidence': query_result['response'].get('confidence', 0.8),
                'user_text': stt_result['text']
            }
            
        except Exception as e:
            logger.error(f"Error processing voice query: {e}")
            return {
                'success': False,
                'error': str(e),
                'text_response': 'An error occurred while processing your voice input. Please try again.',
                'audio_response': None,
                'language': 'en',
                'schemes': [],
                'confidence': 0.0
            }
    
    def _analyze_intent(self, query: str) -> str:
        """Analyze user intent from the query"""
        query_lower = query.lower()
        
        # Intent patterns (English and Kannada)
        intent_patterns = {
            'search_scheme': [
                r'scheme.*for',
                r'program.*for',
                r'yojana.*for',
                r'benefit.*for',
                r'help.*with',
                r'support.*for',
                # Kannada patterns
                r'ಯೋಜನೆ',
                r'ಕಾರ್ಯಕ್ರಮ',
                r'ಲಾಭ',
                r'ಸಹಾಯ',
                r'ಬೆಂಬಲ'
            ],
            'get_info': [
                r'what.*is',
                r'tell.*about',
                r'information.*about',
                r'details.*of',
                r'explain',
                # Kannada patterns
                r'ಏನು',
                r'ಹೇಳಿ',
                r'ಮಾಹಿತಿ',
                r'ವಿವರ',
                r'ವಿವರಿಸಿ'
            ],
            'eligibility': [
                r'eligible',
                r'qualify',
                r'criteria',
                r'requirements',
                r'who.*can.*apply',
                # Kannada patterns
                r'ಅರ್ಹತೆ',
                r'ಅರ್ಹ',
                r'ನಿಯಮ',
                r'ಅವಶ್ಯಕತೆ',
                r'ಯಾರು.*ಅರ್ಜಿ'
            ],
            'application': [
                r'how.*to.*apply',
                r'apply.*for',
                r'application.*process',
                r'where.*to.*apply',
                r'documents.*required',
                # Kannada patterns
                r'ಎಲ್ಲಿ.*ಅರ್ಜಿ',
                r'ಅರ್ಜಿ.*ಹಾಕಿ',
                r'ಅರ್ಜಿ.*ಪ್ರಕ್ರಿಯೆ',
                r'ಎಲ್ಲಿ.*ಅರ್ಜಿ',
                r'ದಾಖಲೆ.*ಅವಶ್ಯಕ'
            ],
            'benefits': [
                r'benefits',
                r'advantages',
                r'what.*do.*i.*get',
                r'assistance',
                r'help.*provided',
                # Kannada patterns
                r'ಲಾಭ',
                r'ಅನುಕೂಲ',
                r'ಏನು.*ಸಿಗುತ್ತದೆ',
                r'ಸಹಾಯ',
                r'ಬೆಂಬಲ.*ನೀಡುತ್ತಾರೆ'
            ],
            'sector_specific': [
                r'agriculture',
                r'health',
                r'education',
                r'employment',
                r'farmer',
                r'student',
                r'job',
                # Kannada patterns
                r'ಕೃಷಿ',
                r'ಆರೋಗ್ಯ',
                r'ಶಿಕ್ಷಣ',
                r'ಉದ್ಯೋಗ',
                r'ರೈತ',
                r'ವಿದ್ಯಾರ್ಥಿ',
                r'ಕೆಲಸ'
            ],
            'greeting': [
                r'hello',
                r'hi',
                r'good.*morning',
                r'good.*afternoon',
                r'good.*evening',
                # Kannada patterns
                r'ನಮಸ್ಕಾರ',
                r'ಹಲೋ',
                r'ಶುಭ.*ಬೆಳಿಗ್ಗೆ',
                r'ಶುಭ.*ಮಧ್ಯಾಹ್ನ',
                r'ಶುಭ.*ಸಂಜೆ'
            ],
            'help': [
                r'help',
                r'what.*can.*you.*do',
                r'how.*to.*use',
                r'commands',
                # Kannada patterns
                r'ಸಹಾಯ',
                r'ಏನು.*ಮಾಡಬಹುದು',
                r'ಹೇಗೆ.*ಬಳಸುವುದು',
                r'ಆಜ್ಞೆಗಳು'
            ]
        }
        
        for intent, patterns in intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    return intent
        
        return 'general_query'
    
    def _extract_keywords(self, query: str) -> List[str]:
        """Extract keywords from the query"""
        # Remove common stop words
        stop_words = {
            'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
            'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
            'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
            'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
            'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
            'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
            'while', 'of', 'at', 'by', 'for', 'with', 'through', 'during', 'before', 'after',
            'above', 'below', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
            'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all',
            'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
            'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'can', 'will', 'just',
            'should', 'now', 'please', 'thank', 'thanks'
        }
        
        # Extract words and phrases
        # First try to find exact scheme names
        scheme_names = [
            'pradhan mantri awas yojana',
            'pmay',
            'awas yojana'
        ]
        query_lower = query.lower()
        for scheme in scheme_names:
            if scheme in query_lower:
                return [scheme]
        
        # If no exact scheme found, extract individual words
        words = re.findall(r'\b\w+\b', query_lower)
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        return keywords[:10]  # Limit to 10 keywords
    
    def _extract_entities(self, query: str) -> Dict:
        """Extract entities from the query"""
        entities = {
            'sectors': [],
            'age_groups': [],
            'genders': [],
            'locations': [],
            'scheme_types': []
        }
        
        query_lower = query.lower()
        
        # Extract sectors
        sector_keywords = {
            'agriculture': ['agriculture', 'farmer', 'farming', 'crop', 'irrigation', 'kisan'],
            'health': ['health', 'medical', 'hospital', 'doctor', 'medicine', 'treatment'],
            'education': ['education', 'school', 'college', 'student', 'scholarship', 'learning'],
            'employment': ['employment', 'job', 'work', 'skill', 'training', 'rogar'],
            'housing': ['housing', 'house', 'home', 'awas', 'pmay', 'residence'],
            'social_welfare': ['welfare', 'pension', 'widow', 'disabled', 'senior', 'social', 'housing', 'house', 'awas'],
            'urban_development': ['urban', 'city', 'housing', 'house', 'awas', 'pmay'],
            'women_empowerment': ['women', 'girl', 'female', 'empowerment', 'beti', 'mahila'],
            'youth_development': ['youth', 'young', 'student', 'youth development']
        }
        
        for sector, keywords in sector_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                entities['sectors'].append(sector)
        
        # Extract age groups
        age_patterns = {
            'children': ['child', 'children', 'kid', 'kids', 'minor', 'under 18'],
            'youth': ['youth', 'young', 'teenager', '18-30', '18-35'],
            'adult': ['adult', 'middle age', '30-60', '35-60'],
            'senior': ['senior', 'elderly', 'old', 'above 60', '60+', 'pension']
        }
        
        for age_group, patterns in age_patterns.items():
            if any(pattern in query_lower for pattern in patterns):
                entities['age_groups'].append(age_group)
        
        # Extract genders
        if any(word in query_lower for word in ['women', 'woman', 'girl', 'female', 'ladies']):
            entities['genders'].append('female')
        if any(word in query_lower for word in ['men', 'man', 'boy', 'male', 'gentlemen']):
            entities['genders'].append('male')
        
        return entities
    
    def _search_schemes(self, query: str, keywords: List[str], entities: Dict, intent: str) -> List[Dict]:
        """Search for relevant schemes based on query using MongoDB"""
        try:
            # Import MongoDB adapter
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from mongodb_adapter import MongoDBAdapter
            
            # Use MongoDB adapter
            adapter = MongoDBAdapter()
            schemes = adapter.search_schemes(query, keywords, entities, intent)
            
            return schemes
            
        except Exception as e:
            logger.error(f"Error searching schemes: {e}")
            return []
    
    def _generate_response(self, query: str, schemes: List[GovernmentScheme], intent: str, language: str) -> Dict:
        """Generate response based on query and found schemes"""
        try:
            if not schemes:
                return {
                    'text': self._get_no_results_response(intent, language),
                    'confidence': 0.5,
                    'intent': intent,
                    'scheme_count': 0
                }
            
            # Generate response based on intent
            if intent == 'greeting':
                response_text = self._get_greeting_response(language)
            elif intent == 'help':
                response_text = self._get_help_response(language)
            elif intent == 'get_info':
                response_text = self._get_info_response(schemes, language)
            elif intent == 'eligibility':
                response_text = self._get_eligibility_response(schemes, language)
            elif intent == 'application':
                response_text = self._get_application_response(schemes, language)
            elif intent == 'benefits':
                response_text = self._get_benefits_response(schemes, language)
            else:
                response_text = self._get_general_response(schemes, query, language)
            
            return {
                'text': response_text,
                'confidence': 0.8,
                'intent': intent,
                'scheme_count': len(schemes)
            }
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {
                'text': self._get_error_response(language),
                'confidence': 0.0,
                'intent': intent,
                'scheme_count': 0
            }
    
    def _get_greeting_response(self, language: str) -> str:
        """Get greeting response"""
        responses = {
            'en': "Hello! I'm your Government Scheme Assistant. I can help you find information about various government schemes. What would you like to know?",
            'hi': "नमस्ते! मैं आपका सरकारी योजना सहायक हूं। मैं आपको विभिन्न सरकारी योजनाओं के बारे में जानकारी देने में मदद कर सकता हूं। आप क्या जानना चाहते हैं?",
            'kn': "ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ ಸರ್ಕಾರಿ ಯೋಜನೆ ಸಹಾಯಕ. ನಾನು ವಿವಿಧ ಸರ್ಕಾರಿ ಯೋಜನೆಗಳ ಬಗ್ಗೆ ಮಾಹಿತಿ ನೀಡಲು ನಿಮಗೆ ಸಹಾಯ ಮಾಡಬಹುದು. ನೀವು ಏನು ತಿಳಿಯಲು ಬಯಸುತ್ತೀರಿ?"
        }
        return responses.get(language, responses['en'])
    
    def _get_help_response(self, language: str) -> str:
        """Get help response"""
        responses = {
            'en': "I can help you with:\n• Finding government schemes by sector (agriculture, health, education, employment)\n• Checking eligibility criteria\n• Understanding benefits and application process\n• Getting scheme details and contact information\n\nJust ask me about any scheme or topic!",
            'hi': "मैं आपकी इन चीजों में मदद कर सकता हूं:\n• क्षेत्र के अनुसार सरकारी योजनाएं खोजना (कृषि, स्वास्थ्य, शिक्षा, रोजगार)\n• पात्रता मानदंड जांचना\n• लाभ और आवेदन प्रक्रिया समझना\n• योजना विवरण और संपर्क जानकारी प्राप्त करना\n\nबस किसी भी योजना या विषय के बारे में पूछें!",
            'kn': "ನಾನು ನಿಮಗೆ ಇವುಗಳಲ್ಲಿ ಸಹಾಯ ಮಾಡಬಹುದು:\n• ಕ್ಷೇತ್ರದ ಪ್ರಕಾರ ಸರ್ಕಾರಿ ಯೋಜನೆಗಳನ್ನು ಹುಡುಕುವುದು (ಕೃಷಿ, ಆರೋಗ್ಯ, ಶಿಕ್ಷಣ, ಉದ್ಯೋಗ)\n• ಅರ್ಹತಾ ಮಾನದಂಡಗಳನ್ನು ಪರಿಶೀಲಿಸುವುದು\n• ಪ್ರಯೋಜನಗಳು ಮತ್ತು ಅರ್ಜಿ ಪ್ರಕ್ರಿಯೆಯನ್ನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳುವುದು\n• ಯೋಜನೆ ವಿವರಗಳು ಮತ್ತು ಸಂಪರ್ಕ ಮಾಹಿತಿ ಪಡೆಯುವುದು\n\nಯಾವುದೇ ಯೋಜನೆ ಅಥವಾ ವಿಷಯದ ಬಗ್ಗೆ ಕೇಳಿ!"
        }
        return responses.get(language, responses['en'])
    
    def _get_info_response(self, schemes: List[Dict], language: str) -> str:
        """Get information response"""
        if not schemes:
            return self._get_no_results_response('get_info', language)
        
        scheme = schemes[0]
        response = f"Here's information about {scheme['title']}:\n\n"
        response += f"Description: {scheme['short_description']}\n\n"
        
        if scheme.get('ministry'):
            response += f"Ministry: {scheme['ministry']}\n"
        if scheme.get('department'):
            response += f"Department: {scheme['department']}\n"
        if scheme.get('eligibility_criteria'):
            response += f"Eligibility: {scheme['eligibility_criteria'][:200]}...\n"
        
        response += f"\nFor more details, visit: {scheme.get('source_url', 'N/A')}"
        
        return response
    
    def _get_eligibility_response(self, schemes: List[Dict], language: str) -> str:
        """Get eligibility response"""
        if not schemes:
            return self._get_no_results_response('eligibility', language)
        
        response = "Here are the eligibility criteria for relevant schemes:\n\n"
        
        for i, scheme in enumerate(schemes[:3], 1):
            response += f"{i}. {scheme['title']}\n"
            if scheme.get('eligibility_criteria'):
                response += f"   Eligibility: {scheme['eligibility_criteria'][:300]}...\n\n"
        
        return response
    
    def _get_application_response(self, schemes: List[Dict], language: str) -> str:
        """Get application process response"""
        if not schemes:
            return self._get_no_results_response('application', language)
        
        response = "Here's how to apply for relevant schemes:\n\n"
        
        for i, scheme in enumerate(schemes[:3], 1):
            response += f"{i}. {scheme['title']}\n"
            if scheme.get('application_process'):
                response += f"   Process: {scheme['application_process'][:300]}...\n"
            if scheme.get('application_link'):
                response += f"   Apply online: {scheme['application_link']}\n\n"
        
        return response
    
    def _get_benefits_response(self, schemes: List[Dict], language: str) -> str:
        """Get benefits response"""
        if not schemes:
            return self._get_no_results_response('benefits', language)
        
        response = "Here are the benefits of relevant schemes:\n\n"
        
        for i, scheme in enumerate(schemes[:3], 1):
            response += f"{i}. {scheme['title']}\n"
            if scheme.get('benefits'):
                response += f"   Benefits: {scheme['benefits'][:300]}...\n\n"
        
        return response
    
    def _get_general_response(self, schemes: List[Dict], query: str, language: str) -> str:
        """Get general response"""
        if not schemes:
            return self._get_no_results_response('general_query', language)
        
        response = f"I found {len(schemes)} relevant scheme(s) for your query:\n\n"
        
        for i, scheme in enumerate(schemes[:5], 1):
            response += f"{i}. {scheme['title']}\n"
            response += f"   Sector: {scheme['sector'].title()}\n"
            response += f"   Description: {scheme['short_description'][:200]}...\n"
            if scheme.get('ministry'):
                response += f"   Ministry: {scheme['ministry']}\n"
            response += f"   More info: {scheme.get('source_url', 'N/A')}\n\n"
        
        return response
    
    def _get_no_results_response(self, intent: str, language: str) -> str:
        """Get response when no schemes are found"""
        responses = {
            'en': "I couldn't find any schemes matching your query. Please try rephrasing your question or ask about a specific sector like agriculture, health, education, or employment.",
            'hi': "मुझे आपके प्रश्न से मेल खाने वाली कोई योजना नहीं मिली। कृपया अपना प्रश्न दोबारा पूछें या कृषि, स्वास्थ्य, शिक्षा या रोजगार जैसे किसी विशिष्ट क्षेत्र के बारे में पूछें।",
            'kn': "ನಿಮ್ಮ ಪ್ರಶ್ನೆಗೆ ಹೊಂದಾಣಿಕೆಯಾಗುವ ಯಾವುದೇ ಯೋಜನೆಗಳು ನನಗೆ ಸಿಗಲಿಲ್ಲ. ದಯವಿಟ್ಟು ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಮತ್ತೆ ಕೇಳಿ ಅಥವಾ ಕೃಷಿ, ಆರೋಗ್ಯ, ಶಿಕ್ಷಣ ಅಥವಾ ಉದ್ಯೋಗದಂತಹ ನಿರ್ದಿಷ್ಟ ಕ್ಷೇತ್ರದ ಬಗ್ಗೆ ಕೇಳಿ."
        }
        return responses.get(language, responses['en'])
    
    def _get_error_response(self, language: str) -> str:
        """Get error response"""
        responses = {
            'en': "I'm sorry, I encountered an error processing your request. Please try again or rephrase your question.",
            'hi': "मुझे खेद है, आपके अनुरोध को संसाधित करने में त्रुटि आई। कृपया पुनः प्रयास करें या अपना प्रश्न दोबारा पूछें।",
            'kn': "ಕ್ಷಮಿಸಿ, ನಿಮ್ಮ ವಿನಂತಿಯನ್ನು ಸಂಸ್ಕರಿಸುವಾಗ ದೋಷ ಸಂಭವಿಸಿದೆ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ ಅಥವಾ ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಮತ್ತೆ ಕೇಳಿ."
        }
        return responses.get(language, responses['en'])
    
    def _format_scheme(self, scheme: Dict) -> Dict:
        """Format scheme for API response"""
        return {
            'id': str(scheme.get('_id', '')),
            'title': scheme.get('title', ''),
            'description': scheme.get('description', ''),
            'short_description': scheme.get('short_description', ''),
            'sector': scheme.get('sector', ''),
            'ministry': scheme.get('ministry', ''),
            'department': scheme.get('department', ''),
            'government_level': scheme.get('government_level', ''),
            'state': scheme.get('state', ''),
            'eligibility_criteria': scheme.get('eligibility_criteria', ''),
            'benefits': scheme.get('benefits', ''),
            'application_process': scheme.get('application_process', ''),
            'application_link': scheme.get('application_link', ''),
            'launch_date': scheme.get('launch_date', ''),
            'last_date': scheme.get('last_date', ''),
            'helpline_number': scheme.get('helpline_number', ''),
            'email': scheme.get('email', ''),
            'website': scheme.get('website', ''),
            'source_url': scheme.get('source_url', ''),
            'keywords': scheme.get('keywords', []),
            'search_tags': scheme.get('search_tags', []),
            'language': scheme.get('language', 'en'),
            'is_active': scheme.get('is_active', True)
        }


# Global chatbot instance
chatbot = GovernmentChatbot()
