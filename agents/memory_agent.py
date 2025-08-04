# agents/memory_agent.py

import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-flash")

MEMORY_FILE = "memory.json"

def _load_memory():
    """Loads the memory from the JSON file."""
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)
    # Return a default structure if the file doesn't exist or is empty
    return {"conversations": [], "last_targets": {}, "custom_context": {}}

def _save_memory(memory):
    """Saves the memory to the JSON file."""
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=4)

def _extract_kv(command: str) -> dict | None:
    """Extracts a key-value pair from a command to remember."""
    prompt = f"""
You are a data extraction tool. From the user's command, extract the key and the value they want to remember.
The key should be in snake_case.

Examples:
- Command: "Remember my name is Alex" -> {{"key": "user_name", "value": "Alex"}}
- Command: "My favorite color is blue" -> {{"key": "favorite_color", "value": "blue"}}
- Command: "My project folder is at D:\\Projects\\Alpha" -> {{"key": "project_folder_path", "value": "D:\\Projects\\Alpha"}}

Now, extract from this command:
"{command}"
"""
    try:
        response = model.generate_content(prompt)
        # Clean up the response to get a valid JSON string
        json_str = response.text.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(json_str)
    except (json.JSONDecodeError, Exception) as e:
        print(f"Error extracting key-value pair: {e}")
        return None

def _get_recall_key(command: str) -> str:
    """Extracts the key for a piece of information the user wants to recall."""
    prompt = f"""
You are a data key extraction tool. From the user's question, determine the key of the information they are asking for.
The key should be in snake_case.

Examples:
- Question: "What is my name?" -> "user_name"
- Question: "What's my favorite color?" -> "favorite_color"
- Question: "Where is my project folder?" -> "project_folder_path"

Now, extract the key from this question:
"{command}"
"""
    response = model.generate_content(prompt)
    return response.text.strip().replace('"', '') # Clean quotes just in case

def handle_memory(command: str) -> str:
    """The main handler for memory operations."""
    # First, classify if it's a 'remember' or 'recall' command
    classification_prompt = f"""
Is the following command asking to 'remember' (store information) or 'recall' (retrieve information)?
Answer with one word: remember or recall.

Command: "{command}"
"""
    response = model.generate_content(classification_prompt)
    action = response.text.strip().lower()

    memory = _load_memory()

    if "remember" in action:
        kv = _extract_kv(command)
        if kv and "key" in kv and "value" in kv:
            key, value = kv["key"], kv["value"]
            memory["custom_context"][key] = value
            _save_memory(memory)
            return f"Okay, I'll remember that {key.replace('_', ' ')} is {value}."
        else:
            return "I couldn't quite figure out what you wanted me to remember. Please try again."

    elif "recall" in action:
        key_to_recall = _get_recall_key(command)
        if key_to_recall and key_to_recall in memory["custom_context"]:
            value = memory["custom_context"][key_to_recall]
            return f"You told me that {key_to_recall.replace('_', ' ')} is {value}."
        else:
            return f"I don't have any information about {key_to_recall.replace('_', ' ')}."
    
    else:
        return "I'm not sure if you wanted me to remember or recall something. Can you clarify?"