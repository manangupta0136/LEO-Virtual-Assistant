import os
import google.generativeai as genai
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

def execute_command(command: str) -> str:
    prompt = f"""
You are a helpful assistant. Convert the user's natural language request into a valid Windows shell command.

ONLY reply with the command. No explanation or extra text.

Example:
Input: open notepad
Output: start notepad

Input: create a folder named test_folder
Output: mkdir test_folder

Now convert this:
{command}
"""
    memory = load_memory()

    try:
        response = model.generate_content(prompt)
        shell_command = response.text.strip()

        if any(x in shell_command.lower() for x in ["shutdown", "format", "del /f", "rmdir", "taskkill"]):
            return "This command is too risky to execute."

        os.system(shell_command)

        memory["last_targets"]["last_command"] = shell_command
        memory["last_targets"]["natural_language"] = command
        save_memory(memory)

        return f"Finished task: `{command}`"
    
    except Exception as e:
        return f"❌ Failed to execute command: {e}"
