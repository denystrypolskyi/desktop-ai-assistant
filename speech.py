import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("Microphone calibration...")
    recognizer.adjust_for_ambient_noise(source, duration=1)
    print("Ready.")

def listen_command():
    with sr.Microphone() as source:
        try:
            print("Listening...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)

            text = recognizer.recognize_google(audio, language="ru-RU")
            return text.lower()

        except sr.WaitTimeoutError:
            return ""

        except sr.UnknownValueError:
            return ""

        except sr.RequestError as e:
            print("Google service error:", e)
            return ""

        except Exception as e:
            print("Microphone error:", repr(e))
            return ""