import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-1.5-flash")

def classify_command(command):
    prompt = f"""
You are an intelligent classifier. Categorize the user's input into one of three categories:

1.  **thinking_body**: If it is an action or task for the system to perform (e.g., "open Chrome", "create a folder").
2.  **memory_agent**: If the command is about remembering, storing, recalling, or forgetting information (e.g., "Remember my name is Leo", "What is my project folder?", "Forget my name").
3.  **thinking_brain**: If it is a general conversation or question (e.g., "what's the capital of France?", "tell me a joke").

Just reply with one category name: thinking_body, memory_agent, or thinking_brain.

Command: "{command}"
Answer:"""

    response = model.generate_content(prompt)
    reply = response.text.strip().lower()

    if "thinking_body" in reply:
        return "thinking_body"
    elif "memory_agent" in reply:
        return "memory_agent"
    else:
        return "thinking_brain"