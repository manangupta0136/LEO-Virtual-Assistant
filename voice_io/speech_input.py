# voice_io/speech_input.py

import speech_recognition as sr

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        # 1. Calibrate for ambient noise
        print("Calibrating... Please wait a moment.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        # 2. You can also adjust the pause threshold if you pause while speaking
        recognizer.pause_threshold = 0.8
        
        print("🎤 Listening...")
        
        try:
            # Listen for the user's input
            audio = recognizer.listen(source)
            
            # Use Google's recognizer to convert speech to text
            text = recognizer.recognize_google(audio)
            print(f"🗣️ You said: {text}")
            return text.lower()

        except sr.UnknownValueError:
            # This error means the recognizer couldn't understand the audio
            # With calibration, this should happen less often.
            print("❗ Could not understand audio.")
        except sr.RequestError as e:
            # This error is for API issues (e.g., no internet)
            print(f"❗ Request error from Google Speech Recognition service; {e}")
        except Exception as e:
            # Catch any other exceptions
            print(f"An error occurred: {e}")

        return ""