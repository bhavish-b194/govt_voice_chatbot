// Translation handling in frontend
class TranslationHandler {
    constructor() {
        this.translations = window.translations || {};
        this.currentLanguage = window.currentLanguage || 'en';
        this.setupLanguageSelector();
    }

    setupLanguageSelector() {
        const languageSelect = document.getElementById('languageSelect');
        if (languageSelect) {
            languageSelect.value = this.currentLanguage;
            languageSelect.addEventListener('change', (e) => {
                this.setLanguage(e.target.value);
            });
        }
    }

    async setLanguage(languageCode) {
        try {
            // Save language preference to session
            const response = await fetch('/chatbot/set_language/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: JSON.stringify({ language: languageCode })
            });

            if (response.ok) {
                this.currentLanguage = languageCode;
                // Reload page to update all translations
                window.location.reload();
            }
        } catch (error) {
            console.error('Error setting language:', error);
        }
    }

    getCsrfToken() {
        // Get CSRF token from cookie
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    translate(key) {
        // Get translation using dot notation (e.g., 'chatbot.welcome_message')
        const parts = key.split('.');
        let current = this.translations;
        
        for (const part of parts) {
            if (current && current[part]) {
                current = current[part];
            } else {
                return key; // Return key if translation not found
            }
        }

        return typeof current === 'string' ? current : key;
    }
}

// Initialize translation handler when document is ready
document.addEventListener('DOMContentLoaded', () => {
    window.translationHandler = new TranslationHandler();
});