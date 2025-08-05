# main.py

from voice_io.speech_input import listen
from voice_io.speech_output import speak
from agents.classifier_agent import classify_command
from agents.thinking_brain_agent import think_and_reply
from agents.thinking_body_agent import execute_command
from agents.memory_agent import handle_memory
from agents.speech_agent import polish_speech
from gui import LEO_GUI
import tkinter as tk
import json
import os

# We keep this here specifically for the "it" resolution feature
MEMORY_FILE = "memory.json"
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)
    return {"conversations": [], "last_targets": {}, "custom_context": {}}


def classify_and_respond(command, should_speak=True):
    """Classifies a command and routes it to the appropriate agent."""
    if not command:
        return "" # Do nothing if there's no command

    # Simple reference resolution for the word "it"
    if "it" in command.lower().split():
        memory = load_memory()
        last_command = memory.get("last_targets", {}).get("natural_language")
        if last_command:
            print(f"Replacing 'it' with context: '{last_command}'")
            command = command.lower().replace("it", last_command)
        else:
            return "I'm not sure what 'it' refers to."

    # Classify the user's command to determine the task type
    task_type = classify_command(command)
    print(f"Task classified as: {task_type}")

    # Route the command to the correct agent
    if task_type == "thinking_brain":
        response = think_and_reply(command)
        print(f"🧠 Brain: {response}")
    elif task_type == "thinking_body":
        response = execute_command(command)
        print(f"🤖 Body: {response}")
    elif task_type == "memory_agent":
        response = handle_memory(command)
        print(f"💾 Memory: {response}")
    else:
        response = "Sorry, I had trouble classifying that command."

    # Polish the agent's response to make it sound more natural
    if should_speak and response:
        cleaned_response = polish_speech(response)
        speak(cleaned_response)

    return response

def run_leo(gui):
    """The main application loop for LEO."""
    gui.add_to_chat_window("LEO", "Session started. I'm ready for your command.")
    while True:
        gui.update_status("Listening...")
        user_input = listen()

        if user_input: # Only process if listen() returned text
            # Add user's command to the chat window
            gui.add_to_chat_window("You", user_input)
            
            # Check for the stop command
            if user_input.strip().lower() == "stop":
                gui.update_status("Stopped")
                response = "LEO has stopped."
                speak(response)
                gui.add_to_chat_window("LEO", f"🛑 {response}")
                gui.start_button.config(state=tk.NORMAL, text="Start LEO") # Re-enable button
                break

            gui.update_status("Processing...")
            response = classify_and_respond(user_input, gui.should_speak())

            # Add LEO's response to the chat window
            gui.add_to_chat_window("LEO", response)
            gui.update_status("Idle")
        else:
            # If listen() returns nothing (e.g., error or silence), update status
            gui.update_status("Listening Error. Try again.")


if __name__ == "__main__":
    root = tk.Tk()
    gui = LEO_GUI(root, run_leo)
    gui.add_to_chat_window("LEO", "Hello! I'm LEO. Click 'Start LEO' to begin.")
    root.mainloop()