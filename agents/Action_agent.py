import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-flash")

MEMORY_FILE = "memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)
    return {"conversations": [], "last_targets": {}, "custom_context": {}}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=4)

def think_and_reply(prompt: str) -> str:
    memory = load_memory()

    try:
        chat = model.start_chat(history=memory["conversations"])
        response = chat.send_message(prompt)

        memory["conversations"].append({"role": "user", "parts": [prompt]})
        memory["conversations"].append({"role": "model", "parts": [response.text]})

        save_memory(memory)

        return response.text
    except Exception as e:
        return f"Thinking error: {str(e)}"
