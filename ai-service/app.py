
# Import Flask framework for creating the web server and handling requests/responses
from flask import Flask, request, jsonify
# Import Hugging Face transformers for NLP models
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
# Import torch for tensor operations (required by transformers)
import torch

# Create a Flask application instance
app = Flask(__name__)

# Load a smaller conversational model for local use
model_name = "microsoft/DialoGPT-medium"  # Name of the pre-trained model
# Load the tokenizer for the model
tokenizer = AutoTokenizer.from_pretrained(model_name)
# Load the model itself
model = AutoModelForCausalLM.from_pretrained(model_name)

# Define a route '/process' that accepts POST requests
@app.route('/process', methods=['POST'])
def process_text():
    # Get the JSON data from the incoming request
    data = request.get_json()
    # Extract the 'text' field from the JSON data, default to empty string if not present
    text = data.get('text', '')
    
    # Generate a response using the model
    # Encode the input text and add the end-of-sequence token
    inputs = tokenizer.encode(text + tokenizer.eos_token, return_tensors='pt')
    # Generate a response from the model with sampling and temperature
    outputs = model.generate(
        inputs, 
        max_length=1000, 
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
        temperature=0.7
    )
    # Decode the generated tokens to get the response text
    response = tokenizer.decode(outputs[:, inputs.shape[-1]:][0], skip_special_tokens=True)
    
    # Return the generated response as JSON
    return jsonify({'response': response})

# If this script is run directly, start the Flask development server
if __name__ == '__main__':
    # Run the app on all available network interfaces (0.0.0.0) and port 5000
    app.run(host='0.0.0.0', port=5000)
