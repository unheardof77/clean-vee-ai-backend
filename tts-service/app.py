
# Import Flask framework for creating the web server
from flask import Flask, request, send_file
# Import gTTS (Google Text-to-Speech), though not used in this file
from gtts import gTTS
# Import pyttsx3 for offline text-to-speech conversion
import pyttsx3
# Import os module for interacting with the operating system (not used here)
import os

# Create a Flask application instance. __name__ is the name of the current Python module
app = Flask(__name__)


# Define a route '/synthesize' that accepts POST requests
@app.route('/synthesize', methods=['POST'])
def synthesize_speech():
    # Get the JSON data from the incoming request
    data = request.get_json()
    # Extract the 'text' field from the JSON data, default to empty string if not present
    text = data.get('text', '')
    
    # Initialize the pyttsx3 engine for offline TTS
    engine = pyttsx3.init()
    # Set the path where the output audio file will be saved
    audio_path = "/app/shared/output.wav"
    # Save the synthesized speech to the specified file
    engine.save_to_file(text, audio_path)
    # Run the speech engine and wait until it finishes processing
    engine.runAndWait()
    
    # Send the generated audio file back to the client as an attachment
    return send_file(audio_path, as_attachment=True)

# If this script is run directly (not imported), start the Flask development server
if __name__ == '__main__':
    # Run the app on all available network interfaces (0.0.0.0) and port 5000
    app.run(host='0.0.0.0', port=5000)
