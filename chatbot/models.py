from django.db import models
from django.contrib.auth.models import User
import json


class GovernmentScheme(models.Model):
    """Model for storing government schemes information"""
    
    SECTOR_CHOICES = [
        ('agriculture', 'Agriculture'),
        ('health', 'Health'),
        ('education', 'Education'),
        ('employment', 'Employment'),
        ('social_welfare', 'Social Welfare'),
        ('rural_development', 'Rural Development'),
        ('urban_development', 'Urban Development'),
        ('women_empowerment', 'Women Empowerment'),
        ('youth_development', 'Youth Development'),
        ('senior_citizens', 'Senior Citizens'),
        ('disability', 'Disability'),
        ('other', 'Other'),
    ]
    
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('hi', 'Hindi'),
        ('kn', 'Kannada'),
        ('ta', 'Tamil'),
        ('te', 'Telugu'),
        ('bn', 'Bengali'),
        ('gu', 'Gujarati'),
        ('mr', 'Marathi'),
        ('pa', 'Punjabi'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=500, help_text="Scheme title")
    description = models.TextField(help_text="Detailed description of the scheme")
    short_description = models.TextField(max_length=1000, help_text="Brief description")
    
    # Categorization
    sector = models.CharField(max_length=50, choices=SECTOR_CHOICES, help_text="Primary sector")
    sub_sectors = models.JSONField(default=list, help_text="Additional sectors this scheme covers")
    
    # Government Information
    ministry = models.CharField(max_length=200, help_text="Responsible ministry")
    department = models.CharField(max_length=200, help_text="Responsible department")
    government_level = models.CharField(
        max_length=20,
        choices=[('central', 'Central'), ('state', 'State'), ('local', 'Local')],
        help_text="Level of government"
    )
    state = models.CharField(max_length=100, blank=True, null=True, help_text="State (if applicable)")
    
    # Eligibility and Benefits
    eligibility_criteria = models.TextField(help_text="Who can apply")
    benefits = models.TextField(help_text="What benefits are provided")
    financial_assistance = models.TextField(blank=True, null=True, help_text="Financial assistance details")
    
    # Application Process
    application_process = models.TextField(help_text="How to apply")
    required_documents = models.JSONField(default=list, help_text="Documents required for application")
    application_link = models.URLField(blank=True, null=True, help_text="Online application link")
    
    # Important Dates
    launch_date = models.DateField(help_text="When the scheme was launched")
    last_date = models.DateField(blank=True, null=True, help_text="Last date to apply")
    validity_period = models.CharField(max_length=100, blank=True, null=True, help_text="Scheme validity period")
    
    # Contact Information
    helpline_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    
    # Multilingual Support
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='en')
    title_translations = models.JSONField(default=dict, help_text="Translations of title in different languages")
    description_translations = models.JSONField(default=dict, help_text="Translations of description")
    
    # Metadata
    source_url = models.URLField(help_text="Source URL where this information was scraped from")
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, help_text="Whether the scheme is currently active")
    
    # Search and Keywords
    keywords = models.JSONField(default=list, help_text="Keywords for search functionality")
    search_tags = models.JSONField(default=list, help_text="Tags for better search and categorization")
    
    class Meta:
        db_table = 'schemes'
        indexes = [
            models.Index(fields=['sector']),
            models.Index(fields=['government_level']),
            models.Index(fields=['state']),
            models.Index(fields=['language']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.sector}"


class ChatSession(models.Model):
    """Model for storing chat sessions"""
    
    session_id = models.CharField(max_length=100, unique=True)
    user_ip = models.GenericIPAddressField(blank=True, null=True)
    language = models.CharField(max_length=10, choices=GovernmentScheme.LANGUAGE_CHOICES, default='en')
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'chat_sessions'
    
    def __str__(self):
        return f"Session {self.session_id} - {self.language}"


class ChatMessage(models.Model):
    """Model for storing individual chat messages"""
    
    MESSAGE_TYPES = [
        ('user', 'User'),
        ('bot', 'Bot'),
        ('system', 'System'),
    ]
    
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES)
    text_content = models.TextField(help_text="Text content of the message")
    audio_file = models.FileField(upload_to='chat_audio/', blank=True, null=True)
    language = models.CharField(max_length=10, choices=GovernmentScheme.LANGUAGE_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # For bot messages
    related_schemes = models.JSONField(default=list, help_text="IDs of schemes mentioned in this response")
    confidence_score = models.FloatField(blank=True, null=True, help_text="Confidence score for the response")
    
    class Meta:
        db_table = 'chat_messages'
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.message_type}: {self.text_content[:50]}..."


class WebScrapingLog(models.Model):
    """Model for logging web scraping activities"""
    
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('partial', 'Partial'),
    ]
    
    source_url = models.URLField()
    source_name = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    schemes_found = models.IntegerField(default=0)
    schemes_added = models.IntegerField(default=0)
    schemes_updated = models.IntegerField(default=0)
    error_message = models.TextField(blank=True, null=True)
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField(blank=True, null=True)
    duration_seconds = models.IntegerField(blank=True, null=True)
    
    class Meta:
        db_table = 'scraping_logs'
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.source_name} - {self.status} - {self.schemes_found} schemes"


class AdminUser(models.Model):
    """Extended user model for admin panel"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=20,
        choices=[('super_admin', 'Super Admin'), ('admin', 'Admin'), ('moderator', 'Moderator')],
        default='admin'
    )
    can_scrape = models.BooleanField(default=True)
    can_manage_schemes = models.BooleanField(default=True)
    can_manage_users = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'admin_users'
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"