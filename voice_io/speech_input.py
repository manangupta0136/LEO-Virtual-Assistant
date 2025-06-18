import speech_recognition as sr

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            print(f"🗣️ You said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("❗ Could not understand audio.")
        except sr.RequestError as e:
            print(f"❗ Request error: {e}")

        return ""
