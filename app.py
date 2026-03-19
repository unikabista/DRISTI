from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, jsonify, send_file
import os
import base64
import cv2
import numpy as np
import time
import speech_recognition as sr

from model.caption import describe_image
from model.speak import speak

app = Flask(__name__)

# Command patterns for English
COMMAND_PATTERNS = [
    'take a photo', 'capture photo', 'take picture', 'capture image', 
    'describe this', 'what do you see', 'describe scene',
    'read the text', 'read text', 'what text do you see', 
    'read what\'s written', 'flip camera', 'switch camera', 'change camera'
]

# Mapping recognized command patterns to actions
ACTION_MAPPING = {
    'capture': ['take a photo', 'capture photo', 'take picture', 'capture image', 
                'describe this', 'what do you see', 'describe scene'],
    'read': ['read the text', 'read text', 'what text do you see', 
             'read what\'s written'],
    'flip': ['flip camera', 'switch camera', 'change camera']
}

def get_action_from_command(command_text):
    """Determines the action based on the command text."""
    command_text_lower = command_text.lower()
    
    for action, patterns in ACTION_MAPPING.items():
        if any(pattern in command_text_lower for pattern in patterns):
            return action
    
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/api/intent", methods=["POST"])
def parse_intent():
    try:
        # Get the spoken command
        user_text = request.json.get("text", "")
        
        # Determine action based on command text
        action = get_action_from_command(user_text)

        if action:
            return jsonify({
                'action': action,
                'status': 'success'
            })
        else:
            return jsonify({
                'action': None,
                'status': 'unrecognized_command'
            })

    except Exception as e:
        print(f"Intent parsing endpoint error: {e}")
        return jsonify({
            'action': None,
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/capture', methods=['POST'])
def capture():
    try:
        # Decode image directly to memory
        data = request.json.get('image', '')
        if not data:
            print("No image data received in request")
            return jsonify({'error': 'No image data provided'}), 400

        print("Received image data, length:", len(data))
        header, encoded = data.split(",", 1)
        img_data = base64.b64decode(encoded)
        nparr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            print("Failed to decode image data")
            return jsonify({'error': 'Failed to decode image'}), 400

        print("Successfully decoded image, shape:", img.shape)
        # Save to temporary file with timestamp
        filename = f'captured_{int(time.time())}.jpg'
        cv2.imwrite(filename, img)
        print("Saved image to:", filename)

        try:
            # Generate description
            print("Calling describe_image function")
            description = describe_image(filename)
            print("Generated description:", description)

            # Speak the description
            speak(description)

            return jsonify({
                'caption': description,
                'status': 'success',
                'message': 'Image processed successfully'
            })
        finally:
            # Clean up the image file
            try:
                os.remove(filename)
                print("Cleaned up temporary image file")
            except Exception as cleanup_error:
                print(f"Error cleaning up image file {filename}: {cleanup_error}")
                pass

    except Exception as e:
        print("Error in /capture:", str(e))
        import traceback
        print("Full traceback:", traceback.format_exc())
        return jsonify({
            'error': str(e),
            'status': 'error',
            'message': 'Failed to process image'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
