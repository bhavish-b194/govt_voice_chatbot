"""
Views for the Government Voice Chatbot
Integrates chatbot logic, voice processing, and MongoDB adapter
"""

import json
import uuid
import tempfile
import os
import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Import our sophisticated backend modules
from .chatbot_logic import chatbot
from .voice_processing import VoiceProcessor
from .models import ChatSession, ChatMessage

logger = logging.getLogger(__name__)

# Initialize voice processor
try:
    voice_processor = VoiceProcessor()
    logger.info("Voice processor initialized successfully")
except Exception as e:
    logger.warning(f"Voice processor initialization failed: {e}")
    voice_processor = None


def home(request):
    """Render the main chatbot interface"""
    return render(request, 'home.html')


@csrf_exempt
@require_http_methods(["POST"])
def voice_api(request):
    """
    Handle voice input from the frontend
    This endpoint processes voice input and returns both text and audio responses
    """
    try:
        # Generate or get session ID
        session_id = request.session.get('session_id')
        if not session_id:
            session_id = str(uuid.uuid4())
            request.session['session_id'] = session_id
        
        # Set chatbot session
        chatbot.set_session(session_id)
        
        # Get language preference (default to English)
        language = request.POST.get('language', 'en')
        chatbot.set_language(language)
        
        # Handle voice input
        if 'audio' in request.FILES:
            # Process uploaded audio file
            audio_file = request.FILES['audio']
            
            # Save audio file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                for chunk in audio_file.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name
            
            try:
                # Process voice query using our sophisticated voice processor
                result = chatbot.process_voice_query(temp_file_path)
                
                if result['success']:
                    return JsonResponse({
                        'success': True,
                        'you': result.get('text_response', ''),
                        'bot': result.get('text_response', ''),
                        'audio_response': result.get('audio_response', ''),
                        'language': result.get('language', 'en'),
                        'schemes': result.get('schemes', []),
                        'confidence': result.get('confidence', 0.8)
                    })
                else:
                    return JsonResponse({
                        'success': False,
                        'error': result.get('error', 'Voice processing failed'),
                        'bot': 'Sorry, I could not process your voice input. Please try again.'
                    })
            
            finally:
                # Clean up temporary file
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
        
        else:
            # Fallback: Use microphone input (for development/testing)
            # This simulates voice input for testing purposes
            return JsonResponse({
                'success': False,
                'error': 'No audio file provided',
                'bot': 'Please provide an audio file or use the microphone.'
            })
    
    except Exception as e:
        logger.error(f"Voice API error: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e),
            'bot': 'Sorry, there was an error processing your request. Please try again.'
        })


@api_view(['POST'])
def text_chat_api(request):
    """
    Handle text-based chat queries
    This endpoint processes text input and returns relevant scheme information
    """
    try:
        data = request.data
        query = data.get('query', '').strip()
        language = data.get('language', 'en')
        
        if not query:
            return Response({
                'success': False,
                'error': 'Query is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate or get session ID
        session_id = request.session.get('session_id')
        if not session_id:
            session_id = str(uuid.uuid4())
            request.session['session_id'] = session_id
        
        # Set chatbot session and language
        chatbot.set_session(session_id)
        chatbot.set_language(language)
        
        # Process the query using our sophisticated chatbot logic
        result = chatbot.process_query(query, language)
        
        if result['success']:
            return Response({
                'success': True,
                'response': result['response']['text'],
                'schemes': result['schemes'],
                'intent': result['intent'],
                'keywords': result['keywords'],
                'language': result['language'],
                'confidence': result['response'].get('confidence', 0.8),
                'scheme_count': len(result['schemes'])
            })
        else:
            return Response({
                'success': False,
                'error': result.get('error', 'Query processing failed'),
                'response': result['response']['text']
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    except Exception as e:
        logger.error(f"Text chat API error: {e}")
        return Response({
            'success': False,
            'error': str(e),
            'response': 'Sorry, there was an error processing your request. Please try again.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def chat_history_api(request, session_id):
    """
    Get chat history for a specific session
    """
    try:
        session = ChatSession.objects.get(session_id=session_id)
        messages = ChatMessage.objects.filter(session=session).order_by('timestamp')
        
        history = []
        for message in messages:
            history.append({
                'type': message.message_type,
                'content': message.text_content,
                'timestamp': message.timestamp.isoformat(),
                'language': message.language,
                'confidence': message.confidence_score,
                'related_schemes': message.related_schemes
            })
        
        return Response({
            'success': True,
            'session_id': session_id,
            'language': session.language,
            'message_count': len(history),
            'messages': history
        })
    
    except ChatSession.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Session not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        logger.error(f"Chat history API error: {e}")
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def scheme_search_api(request):
    """
    Search for government schemes
    """
    try:
        query = request.GET.get('q', '').strip()
        sector = request.GET.get('sector', '')
        language = request.GET.get('language', 'en')
        limit = int(request.GET.get('limit', 10))
        
        if not query:
            return Response({
                'success': False,
                'error': 'Query parameter "q" is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Use chatbot logic to search schemes
        chatbot.set_language(language)
        result = chatbot.process_query(query, language)
        
        if result['success']:
            schemes = result['schemes'][:limit]
            return Response({
                'success': True,
                'query': query,
                'scheme_count': len(schemes),
                'schemes': schemes,
                'language': language
            })
        else:
            return Response({
                'success': False,
                'error': 'Search failed',
                'schemes': []
            })
    
    except Exception as e:
        logger.error(f"Scheme search API error: {e}")
        return Response({
            'success': False,
            'error': str(e),
            'schemes': []
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def supported_languages_api(request):
    """
    Get list of supported languages
    """
    languages = [
        {'code': 'en', 'name': 'English'},
        {'code': 'hi', 'name': 'Hindi'},
        {'code': 'kn', 'name': 'Kannada'},
        {'code': 'ta', 'name': 'Tamil'},
        {'code': 'te', 'name': 'Telugu'},
        {'code': 'bn', 'name': 'Bengali'},
        {'code': 'gu', 'name': 'Gujarati'},
        {'code': 'mr', 'name': 'Marathi'},
        {'code': 'pa', 'name': 'Punjabi'}
    ]
    
    return Response({
        'success': True,
        'languages': languages,
        'default_language': 'en'
    })


@api_view(['GET'])
def available_sectors_api(request):
    """
    Get list of available sectors
    """
    sectors = [
        {'code': 'agriculture', 'name': 'Agriculture'},
        {'code': 'health', 'name': 'Health'},
        {'code': 'education', 'name': 'Education'},
        {'code': 'employment', 'name': 'Employment'},
        {'code': 'social_welfare', 'name': 'Social Welfare'},
        {'code': 'rural_development', 'name': 'Rural Development'},
        {'code': 'urban_development', 'name': 'Urban Development'},
        {'code': 'women_empowerment', 'name': 'Women Empowerment'},
        {'code': 'youth_development', 'name': 'Youth Development'},
        {'code': 'senior_citizens', 'name': 'Senior Citizens'},
        {'code': 'disability', 'name': 'Disability'}
    ]
    
    return Response({
        'success': True,
        'sectors': sectors
    })


@api_view(['POST'])
def advanced_search_api(request):
    """
    Advanced search API with filters and sorting
    """
    try:
        # Get search parameters
        data = json.loads(request.body)
        sector = data.get('sector', '')
        ministry = data.get('ministry', '')
        eligibility = data.get('eligibility', '')
        sort_by = data.get('sortBy', 'relevance')
        language = data.get('language', 'en')
        
        # Generate session ID
        session_id = request.session.get('session_id')
        if not session_id:
            session_id = str(uuid.uuid4())
            request.session['session_id'] = session_id
        
        # Set chatbot language and session
        chatbot.set_language(language)
        chatbot.set_session(session_id)
        
        # Build advanced search query
        search_query = "Show me government schemes"
        keywords = []
        entities = {}
        
        if sector:
            search_query += f" in {sector} sector"
            keywords.append(sector)
            entities['sectors'] = [sector]
        
        if ministry:
            search_query += f" from {ministry} ministry"
            keywords.append(ministry)
            entities['ministry'] = ministry
        
        if eligibility:
            search_query += f" for {eligibility}"
            keywords.extend(eligibility.split())
            entities['eligibility'] = eligibility
        
        # Perform advanced search using MongoDB adapter
        from mongodb_adapter import MongoDBAdapter
        mongodb_adapter = MongoDBAdapter()
        
        # Enhanced search with additional filters
        schemes = mongodb_adapter.advanced_search(
            query=search_query,
            keywords=keywords,
            entities=entities,
            sector=sector,
            ministry=ministry,
            eligibility=eligibility,
            sort_by=sort_by
        )
        
        # Generate response message
        if schemes:
            response_msg = f"Found {len(schemes)} government schemes"
            if sector:
                response_msg += f" in {sector} sector"
            if ministry:
                response_msg += f" from {ministry} ministry"
            if eligibility:
                response_msg += f" for {eligibility}"
            response_msg += f", sorted by {sort_by}."
        else:
            response_msg = "No schemes found matching your search criteria. Try adjusting your filters or using different keywords."
        
        # Save search to chat history
        try:
            ChatMessage.objects.create(
                session=chatbot.session,
                message_type='user',
                text_content=search_query,
                language=language,
                related_schemes=[str(scheme.get('_id', '')) for scheme in schemes[:5]]  # Store up to 5 scheme IDs
            )
            
            ChatMessage.objects.create(
                session=chatbot.session,
                message_type='bot',
                text_content=response_msg,
                language=language,
                related_schemes=[str(scheme.get('_id', '')) for scheme in schemes[:5]]
            )
        except Exception as e:
            logger.warning(f"Failed to save advanced search to chat history: {e}")
        
        return Response({
            'success': True,
            'response': response_msg,
            'schemes': schemes,
            'search_params': {
                'sector': sector,
                'ministry': ministry,
                'eligibility': eligibility,
                'sort_by': sort_by,
                'language': language
            },
            'total_results': len(schemes)
        })
    
    except json.JSONDecodeError:
        return Response({
            'success': False,
            'error': 'Invalid JSON data',
            'schemes': []
        }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        logger.error(f"Advanced search API error: {e}")
        return Response({
            'success': False,
            'error': str(e),
            'schemes': []
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)