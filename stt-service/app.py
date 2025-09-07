
# Import Flask framework for creating the web server and handling requests/responses
from flask import Flask, request, jsonify
# Import speech_recognition for speech-to-text processing
import speech_recognition as sr
# Import os for file path operations (not used here)
import os
# Import AudioSegment from pydub for audio format conversion
from pydub import AudioSegment

# Create a Flask application instance
app = Flask(__name__)

# Define a route '/transcribe' that accepts POST requests
@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    # Check if the request contains an 'audio' file
    if 'audio' not in request.files:
        # Return an error if no audio file is provided
        return jsonify({'error': 'No audio file provided'}), 400
    
    # Get the uploaded audio file from the request
    audio_file = request.files['audio']
    # Set the path to save the uploaded audio file in the shared directory
    audio_path = f"/app/shared/{audio_file.filename}"
    # Save the uploaded audio file to the specified path
    audio_file.save(audio_path)
    
    # Convert the audio file to WAV format if it is not already a WAV file
    if not audio_path.endswith('.wav'):
        # Load the audio file using pydub
        sound = AudioSegment.from_file(audio_path)
        # Create a new file path with .wav extension
        wav_path = audio_path.rsplit('.', 1)[0] + '.wav'
        # Export the audio in WAV format
        sound.export(wav_path, format="wav")
        # Update the audio_path to point to the new WAV file
        audio_path = wav_path
    
    # Create a Recognizer instance for speech recognition
    r = sr.Recognizer()
    # Open the audio file for reading
    with sr.AudioFile(audio_path) as source:
        # Record the entire audio file
        audio = r.record(source)
    
    try:
        # Use Google's speech recognition to transcribe the audio
        text = r.recognize_google(audio)  # You can replace with a local model later
        # Return the transcribed text as JSON
        return jsonify({'text': text})
    except sr.UnknownValueError:
        # Return an error if the audio could not be understood
        return jsonify({'error': 'Could not understand audio'}), 400
    except sr.RequestError as e:
        # Return an error if there was a problem with the recognition service
        return jsonify({'error': f'Recognition error: {e}'}), 500

# If this script is run directly, start the Flask development server
if __name__ == '__main__':
    # Run the app on all available network interfaces (0.0.0.0) and port 5000
    app.run(host='0.0.0.0', port=5000)
