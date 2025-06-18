import os
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-1.5-flash")

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

    try:
        response = model.generate_content(prompt)
        shell_command = response.text.strip()

        #avoids shutdown, format, or dangerous commands
        if any(x in shell_command.lower() for x in ["shutdown", "format", "del /f", "rmdir", "taskkill"]):
            return "This command is too risky to execute."

        os.system(shell_command)
        return f"✅ Executed: `{shell_command}`"
    
    except Exception as e:
        return f"❌ Failed to execute command: {e}"
