from handlers import apps, music, volume, pc
from nlu import parse_command
from llm import ask_llm
from tts import speak_jarvis
from utils import clean_text_for_tts
import speech

MODE = "voice" # console | voice
voice_enabled = True

def get_command():
    if MODE == "voice":
        return speech.listen_command()
    return input("You: ").strip()

def respond(text):
    print("Jarvis:", text)
    if voice_enabled:
        speak_jarvis(clean_text_for_tts(text))

if __name__ == "__main__":
    if voice_enabled:
        speak_jarvis("Hi! I am Jarvis, your assistant.")

    while True:
        try:
            cmd = get_command()
            if not cmd:
                continue
            if MODE == "voice":
                print(f"Recognized: {cmd}")

            intent, entity, value, system_command = parse_command(cmd)

            if system_command:
                if volume.handle_volume(intent, value, voice=voice_enabled):
                    continue
                if music.handle_music(intent, value, voice=voice_enabled):
                    continue
                if apps.handle_apps(intent, entity, voice=voice_enabled):
                    continue
                if pc.handle_pc_commands(intent, value, voice=voice_enabled):
                    continue
            elif value: 
                answer = ask_llm(value)
                respond(answer)

        except Exception as e:
            print("Unhandled error:", e)