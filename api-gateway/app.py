from flask import Flask, request, jsonify, send_file
import requests
import os

app = Flask(__name__)

# Service URLs
STT_URL = "http://stt-service:5000/transcribe"
TTS_URL = "http://tts-service:5000/synthesize"
AI_URL = "http://ai-service:5000/process"

@app.route('/ask', methods=['POST'])
def ask_jarvis():
    # Handle audio input
    if 'audio' in request.files:
        audio_file = request.files['audio']
        files = {'audio': (audio_file.filename, audio_file.stream, audio_file.mimetype)}
        stt_response = requests.post(STT_URL, files=files)
        if stt_response.status_code != 200:
            return jsonify({'error': 'Speech recognition failed'}), 500
        text = stt_response.json()['text']
    else:
        data = request.get_json()
        text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    # Process with AI
    ai_response = requests.post(AI_URL, json={'text': text})
    if ai_response.status_code != 200:
        return jsonify({'error': 'AI processing failed'}), 500
    response_text = ai_response.json()['response']
    
    # Generate speech if requested
    if 'audio' in request.args and request.args['audio'].lower() == 'true':
        tts_response = requests.post(TTS_URL, json={'text': response_text})
        if tts_response.status_code != 200:
            return jsonify({'error': 'Speech synthesis failed'}), 500
        
        return send_file(
            "/app/shared/output.wav",
            as_attachment=True,
            download_name="response.wav"
        )
    
    return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
