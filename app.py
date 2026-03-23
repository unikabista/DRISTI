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
from langdetect import detect as detect_lang

app = Flask(__name__)

# Current language setting: "english", "nepali", or "hindi"
current_language = "english"

LANGUAGE_DISPLAY = {
    "english": "English",
    "nepali":  "Nepali",
    "hindi":   "Hindi"
}

# Maps langdetect codes to our internal language keys
LANGDETECT_MAP = {
    "en": "english",
    "hi": "hindi",
    "ne": "nepali"
}

# Maps our internal language keys to BCP-47 codes for frontend speech recognition
LANGUAGE_BCP47 = {
    "english": "en-US",
    "nepali":  "ne-NP",
    "hindi":   "hi-IN"
}

# Mapping recognized command patterns to actions
ACTION_MAPPING = {
    'capture': [
        'take a photo', 'capture photo', 'take picture', 'capture image',
        'describe this', 'what do you see', 'describe scene',
        # Nepali
        'फोटो खिच', 'फोटो लिनुस', 'यो के हो', 'वर्णन गर',
        # Hindi
        'फोटो लो', 'तस्वीर लो', 'यह क्या है', 'वर्णन करो'
    ],
    'read': [
        'read the text', 'read text', 'what text do you see', "read what's written",
        # Nepali
        'पाठ पढ', 'के लेखेको छ',
        # Hindi
        'पाठ पढ़ो', 'क्या लिखा है'
    ],
    'flip': [
        'flip camera', 'switch camera', 'change camera',
        # Nepali
        'क्यामेरा फेर', 'क्यामेरा बदल',
        # Hindi
        'कैमरा बदलो', 'कैमरा पलटो'
    ],
    'language_english': [
        'switch to english', 'change to english', 'speak english', 'english please'
    ],
    'language_nepali': [
        'switch to nepali', 'change to nepali', 'speak nepali',
        'नेपालीमा बोल', 'नेपाली भाषा'
    ],
    'language_hindi': [
        'switch to hindi', 'change to hindi', 'speak hindi',
        'हिंदी में बोलो', 'हिंदी भाषा'
    ]
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

@app.route('/api/language', methods=['POST'])
def set_language():
    global current_language
    lang = request.json.get('language', 'english').lower()
    if lang not in LANGUAGE_DISPLAY:
        return jsonify({'status': 'error', 'message': 'Unsupported language'}), 400
    current_language = lang
    return jsonify({'status': 'success', 'language': current_language})

@app.route("/api/intent", methods=["POST"])
def parse_intent():
    try:
        # Get the spoken command
        user_text = request.json.get("text", "")

        # Auto-detect language from spoken text
        global current_language
        try:
            detected_code = detect_lang(user_text)
            if detected_code in LANGDETECT_MAP:
                current_language = LANGDETECT_MAP[detected_code]
        except Exception:
            pass  # Keep existing language if detection fails

        # Determine action based on command text
        action = get_action_from_command(user_text)

        return jsonify({
            'action': action,
            'status': 'success' if action else 'unrecognized_command',
            'language': current_language,
            'lang_code': LANGUAGE_BCP47[current_language]
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
            description = describe_image(filename, language=LANGUAGE_DISPLAY[current_language])
            print("Generated description:", description)

            return jsonify({
                'caption': description,
                'status': 'success',
                'message': 'Image processed successfully',
                'language': current_language,
                'lang_code': LANGUAGE_BCP47[current_language]
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
