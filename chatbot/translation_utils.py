"""
Translation utility for the chatbot
Handles loading and serving translations for different languages
"""

import json
import os
from django.conf import settings
from functools import lru_cache
from typing import Tuple
import requests

# Optional: URL for an external translation service (LibreTranslate compatible)
LIBRETRANSLATE_URL = os.getenv('LIBRETRANSLATE_URL')
LIBRETRANSLATE_API_KEY = os.getenv('LIBRETRANSLATE_API_KEY')

class Translator:
    def __init__(self):
        self.translations = {}
        self.load_translations()
    
    @lru_cache(maxsize=None)
    def load_translations(self):
        """Load all translation files"""
        translations_dir = os.path.join(settings.BASE_DIR, 'translations')
        for filename in os.listdir(translations_dir):
            if filename.endswith('.json'):
                language_code = filename[:-5]  # Remove .json
                file_path = os.path.join(translations_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.translations[language_code] = json.load(f)
    
    def get_text(self, key: str, language: str = 'en') -> str:
        """
        Get translated text for a key in specified language
        Args:
            key: Dot notation key (e.g., 'chatbot.welcome_message')
            language: Language code (e.g., 'en', 'kn', 'hi')
        Returns:
            Translated text or key if translation not found
        """
        try:
            # Split the key into parts (e.g., ['chatbot', 'welcome_message'])
            parts = key.split('.')
            
            # Navigate through the translations dictionary
            current = self.translations.get(language, {})
            for part in parts:
                current = current.get(part, None)
                if current is None:
                    # Fall back to English if translation not found
                    current = self.translations.get('en', {})
                    for p in parts:
                        current = current.get(p, key)
                    break
            
            return current if isinstance(current, str) else key
        except Exception:
            return key
    
    def get_all_translations(self, language: str) -> dict:
        """Get all translations for a language"""
        return self.translations.get(language, {})

# Create a global translator instance
translator = Translator()

# Convenience function
def _(key: str, language: str = 'en') -> str:
    """Shorthand for translator.get_text"""
    return translator.get_text(key, language)


def translate_text(text: str, target_language: str = 'en') -> Tuple[str, bool, str]:
    """
    Translate a given text into the target language.

    Strategy:
    1. If an exact match exists in our local translations under top-level keys (e.g. 'schemes'), return it.
    2. If LIBRETRANSLATE_URL is configured, call the service to translate.
    3. Otherwise, return the original text and indicate translation was not performed.

    Returns: (translated_text, translated_flag, source)
        source: 'local' | 'libre' | 'none'
    """
    if not text:
        return text, False, 'none'

    # 1) Try local exact lookup in translations (searching shallowly across categories)
    try:
        for lang_code, data in translator.translations.items():
            # only check for requested target language
            if lang_code != target_language:
                continue
            # Search for the exact text in English translation values and map
            # This requires that static strings are present in both languages in the JSON files
            # We'll search under 'schemes' and other top-level nodes
            candidates = data.get('schemes', {})
            # If any of the values equal the original English text, return the localized value
            # Note: This is a conservative exact-match check
            for k, v in candidates.items():
                # if value equals text (unlikely), return it. More commonly we won't find matches here.
                if isinstance(v, str) and v.strip() == text.strip():
                    return v, True, 'local'
    except Exception:
        # ignore any issues with local lookup
        pass

    # 2) Try external LibreTranslate-like service if configured
    if LIBRETRANSLATE_URL:
        try:
            payload = {
                'q': text,
                'source': 'en',
                'target': target_language,
                'format': 'text'
            }
            headers = {'Accept': 'application/json'}
            if LIBRETRANSLATE_API_KEY:
                headers['Authorization'] = f'Bearer {LIBRETRANSLATE_API_KEY}'

            resp = requests.post(f"{LIBRETRANSLATE_URL.rstrip('/')}/translate", json=payload, headers=headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                translated = data.get('translatedText') or data.get('result') or data.get('translated_text')
                if translated:
                    return translated, True, 'libre'
        except Exception:
            # network/timeout error - fall through to returning original
            pass

    # 3) No translation available
    return text, False, 'none'