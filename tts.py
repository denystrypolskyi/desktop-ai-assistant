import io
import os
from dotenv import load_dotenv
import requests
import pygame
import pyttsx3

pygame.mixer.init()

USE_ELEVENLABS = False

load_dotenv()

API_KEY = os.getenv("TTS_API_KEY")
VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"

def speak_jarvis(text: str):
    if USE_ELEVENLABS:
        try:
            pygame.mixer.init()

            url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}?output_format=mp3_44100_128"
            headers = {"xi-api-key": API_KEY, "Content-Type": "application/json"}
            data = {"text": text, "model_id": "eleven_multilingual_v2"}

            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()

            audio_bytes = io.BytesIO(response.content)
            pygame.mixer.music.load(audio_bytes)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

        except Exception as e:
            print("ElevenLabs TTS error:", e)
    else:
        try:
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print("Local TTS error:", e)