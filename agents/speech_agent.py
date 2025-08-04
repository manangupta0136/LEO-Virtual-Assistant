# agents/speech_agent.py

import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure the API key once
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-1.5-flash")

def polish_speech(text: str) -> str:
    prompt = f"""
You are an agent that prepares AI responses for voice output. Your job is to clean up technical or verbose responses and make them sound friendly and natural for speech.

Here are your rules:
1.  Remove markdown like ** or *.
2.  Simplify file/folder paths. For example: "Executed: `mkdir C:/Users/Leo/Desktop/New Folder`" → "Your new folder is ready on the desktop."
3.  Avoid robotic phrases like "Command executed" or "Executing". Instead, use phrases like "Done," "All set," or "Okay, finished."
4.  If the input is about opening an app, be brief. "Opening Google Chrome" → "Opening Chrome."
5.  When a command execution result is given (like "✅ Executed: `mkdir LEO`"), turn it into a natural confirmation ("Okay, I've created the LEO folder.").
6.  Randomize your endings sometimes.

Now, polish this response for speaking:
\"\"\"{text}\"\"\"
"""
    
    try:
        # Generate the polished text
        response = model.generate_content(prompt)
        polished_text = response.text.strip()
        # Return ONLY the polished text
        return polished_text
    
    except Exception as e:
        print(f"Speech polishing error: {e}")
        # Fallback to the original text if polishing fails
        return text