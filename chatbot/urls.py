from django.urls import path
from . import views

urlpatterns = [
    # Main interface
    path('', views.home, name='home'),
    
    # Voice and text chat endpoints
    path('voice/', views.voice_api, name='voice_api'),
    path('api/chat/text/', views.text_chat_api, name='text_chat_api'),
    path('api/chat/voice/', views.voice_api, name='voice_chat_api'),
    
    # Chat history
    path('api/chat/history/<str:session_id>/', views.chat_history_api, name='chat_history_api'),
    
    # Scheme search and information
    path('api/schemes/search/', views.scheme_search_api, name='scheme_search_api'),
    path('api/chat/advanced-search/', views.advanced_search_api, name='advanced_search_api'),
    path('api/schemes/languages/', views.supported_languages_api, name='supported_languages_api'),
    path('api/schemes/sectors/', views.available_sectors_api, name='available_sectors_api'),
]