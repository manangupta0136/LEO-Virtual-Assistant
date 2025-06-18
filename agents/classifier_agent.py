import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-1.5-flash")

def classify_command(command):
    prompt = f"""
You are an intelligent classifier. Categorize the user's input into one of two categories:
1. thinking_brain - if it is a conversation or question
2. thinking_body - if it is an action or task for the system to perform

Just reply with one word: thinking_brain or thinking_body

Command: "{command}"
Answer:"""

    response = model.generate_content(prompt)
    reply = response.text.strip().lower()

    if "thinking_body" in reply:
        return "thinking_body"
    else:
        return "thinking_brain"
