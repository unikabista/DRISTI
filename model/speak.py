import speech_recognition as sr
import os
import pyaudio
from google import genai
from google.genai import types

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

LANGUAGE_CODES = {
    "english": "en-US",
    "nepali":  "ne-NP",
    "hindi":   "hi-IN"
}

def detect_speech(language="english"):
    """Detect speech from user's microphone"""
    recognizer = sr.Recognizer()
    lang_code = LANGUAGE_CODES.get(language.lower(), "en-US")
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language=lang_code)
            return text
        except Exception as e:
            print(f"Speech recognition error: {e}")
    return None

def speak(text):
    """Speak the given text using Gemini TTS (auto-detects language from text)"""
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-tts",
            contents=text,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name="Kore",
                        )
                    )
                ),
            ),
        )

        audio_data = response.candidates[0].content.parts[0].inline_data.data

        # Play raw PCM audio (24kHz, 16-bit, mono)
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)
        stream.write(audio_data)
        stream.stop_stream()
        stream.close()
        p.terminate()

    except Exception as e:
        print(f"Speech Error: {e}")
