class VoiceHandler {
    constructor(options = {}) {
        this.onStart = options.onStart || (() => {});
        this.onStop = options.onStop || (() => {});
        this.onError = options.onError || (() => {});
        this.onDataAvailable = options.onDataAvailable || (() => {});
        
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.isRecording = false;
        this.stream = null;
    }

    async startRecording() {
        try {
            // Request microphone access with specific audio constraints
            const stream = await navigator.mediaDevices.getUserMedia({
                audio: {
                    echoCancellation: true,
                    noiseSuppression: true,
                    sampleRate: 44100,
                    channelCount: 1
                }
            });
            
            this.stream = stream;
            this.audioChunks = [];
            
            // Create media recorder with optimal settings
            this.mediaRecorder = new MediaRecorder(stream, {
                mimeType: this.getSupportedMimeType(),
                audioBitsPerSecond: 128000
            });
            
            // Set up event handlers
            this.mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    this.audioChunks.push(event.data);
                }
            };
            
            this.mediaRecorder.onstart = () => {
                this.isRecording = true;
                this.onStart();
                console.log('Recording started');
            };
            
            this.mediaRecorder.onstop = async () => {
                this.isRecording = false;
                if (this.stream) {
                    this.stream.getTracks().forEach(track => track.stop());
                }
                
                const audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
                this.onStop(audioBlob);
                console.log('Recording stopped');
            };
            
            // Start recording
            this.mediaRecorder.start();
            
        } catch (error) {
            console.error('Error starting recording:', error);
            this.onError(error);
        }
    }

    stopRecording() {
        if (this.mediaRecorder && this.isRecording) {
            this.mediaRecorder.stop();
        }
    }

    getSupportedMimeType() {
        const types = [
            'audio/webm',
            'audio/wav',
            'audio/ogg',
            'audio/mp4'
        ];
        
        for (const type of types) {
            if (MediaRecorder.isTypeSupported(type)) {
                return type;
            }
        }
        
        return 'audio/webm'; // Fallback
    }

    isSupported() {
        return !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia);
    }
}