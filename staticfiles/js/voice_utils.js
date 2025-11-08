// Voice recording status messages
const VOICE_STATUS = {
    INITIALIZING: 'Initializing voice input...',
    READY: 'Ready for voice input',
    RECORDING: 'Recording... Click stop when finished',
    PROCESSING: 'Processing your voice input...',
    ERROR: 'Error with voice input. Please try again.',
    NO_PERMISSION: 'Please allow microphone access to use voice features.',
    NO_SUPPORT: 'Your browser doesn\'t support voice input. Please use Chrome.',
    FILE_TOO_LARGE: 'Recording too long. Please keep it under 30 seconds.',
    NO_SPEECH: 'No speech detected. Please try again.',
};

function showVoiceStatus(message, isError = false) {
    const statusDiv = document.getElementById('voiceStatus');
    if (!statusDiv) return;
    
    statusDiv.textContent = message;
    statusDiv.className = isError ? 'voice-status error' : 'voice-status';
}

function showVoiceError(error) {
    console.error('Voice Error:', error);
    let message = VOICE_STATUS.ERROR;
    
    if (error.name === 'NotAllowedError') {
        message = VOICE_STATUS.NO_PERMISSION;
    } else if (error.name === 'NotSupportedError') {
        message = VOICE_STATUS.NO_SUPPORT;
    }
    
    showVoiceStatus(message, true);
    
    // Add error to chat as system message
    const chatMessages = document.getElementById('chatMessages');
    if (chatMessages) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'message system';
        errorDiv.innerHTML = `
            <div class="message-content error">
                <i class="fas fa-exclamation-circle"></i>
                ${message}
            </div>
        `;
        chatMessages.appendChild(errorDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

// Voice recording helper functions
function formatAudioData(blob) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = () => reject(reader.error);
        reader.readAsDataURL(blob);
    });
}