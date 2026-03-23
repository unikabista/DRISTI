from PIL import Image
import pytesseract
import cv2
import numpy as np
import base64
import requests
from io import BytesIO
import os

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Eden AI API configuration (read from environment)
EDEN_AI_API_KEY = os.environ.get("EDEN_AI_API_KEY")
EDEN_AI_URL = "https://api.edenai.run/v2/llm/chat"

if not EDEN_AI_API_KEY:
    raise RuntimeError(
        "EDEN_AI_API_KEY environment variable is not set.\n"
        "Add it to your .env file or set it in the environment."
    )

def extract_text(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding to preprocess the image
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
    # Apply dilation to connect text components
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    gray = cv2.dilate(gray, kernel, iterations=1)
    
    # Perform OCR
    text = pytesseract.image_to_string(gray)
    return text.strip()

def get_image_description(base64_image, language="English"):
    """Get image description from GPT-4o using Eden AI API"""
    headers = {
        "Authorization": f"Bearer {EDEN_AI_API_KEY}",
        "Content-Type": "application/json"
    }

    # Prepare the prompt for image description
    prompt = f"""Describe this scene naturally in {language}, as if you're telling a friend what you're looking at.
    Focus on what would be most helpful for a blind person:
    - If people are present, describe their gender, approximate age, and what they're doing
    - What objects and people are present
    - The colors and visual elements
    - How things are arranged in the space
    - Any text that might be important

    Keep it conversational and natural, avoiding phrases like 'the image shows' or 'I can see'.
    Be descriptive but concise. Focus on concrete details rather than subjective atmosphere descriptions.
    When describing people, be specific about their gender, age group, and actions.
    Respond entirely in {language}."""
    
    payload = {
        "model": "openai/gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    }
    
    try:
        response = requests.post(EDEN_AI_URL, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        result = response.json()
        print("API Response:", result)  # Print full API response for debugging
        
        if 'choices' in result and len(result['choices']) > 0:
            return result['choices'][0]['message']['content']
        else:
            print("Unexpected API response format:", result)
            return "Sorry, I couldn't generate a description. API returned unexpected format."
            
    except requests.exceptions.RequestException as e:
        print(f"Network error calling Eden AI API: {e}")
        return "Sorry, there was a network error processing the image."
    except Exception as e:
        print(f"Error calling Eden AI API: {e}")
        return "Sorry, there was an error processing the image."

def describe_image(image_path, language="English"):
    """Describe image using GPT-4o and extract text using OCR"""
    try:
        # Read image for OCR
        cv_image = cv2.imread(image_path)

        # Extract text using OCR
        text = extract_text(cv_image)

        # Convert image to base64 for GPT-4o
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')

        # Get description from GPT-4o
        description = get_image_description(base64_image, language=language)

        # Only add text information if text was actually found
        if text and text.strip():
            return f"{description} The text in the image reads: {text}"
        return description
        
    except Exception as e:
        print(f"Error in describe_image: {e}")
        return "Sorry, I couldn't process the image."
