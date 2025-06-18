import pyttsx3

def speak(text: str):
    engine = pyttsx3.init()
    
    engine.setProperty('rate', 180)      # Speed (words per minute)
    engine.setProperty('volume', 1.0)    # Volume (0.0 to 1.0)

    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # voices[0] = male, voices[1] = female

    engine.say(text)
    engine.runAndWait()
