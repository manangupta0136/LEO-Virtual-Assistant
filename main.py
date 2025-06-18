from voice_io.speech_input import listen
from agents.classifier_agent import classify_command
from agents.thinking_brain_agent import think_and_reply
from agents.thinking_body_agent import execute_command
from voice_io.speech_output import speak

while True:
    command = listen()
    if command.strip() == "stop":
        print("🛑 Stopping...")
        break

    task_type = classify_command(command)

    if task_type == "thinking_brain":
        response = think_and_reply(command)
        print(f"🧠 LEO: {response}")
        speak(response)
    elif task_type == "thinking_body":
        response = execute_command(command)
        print(f"🤖 Body: {response}")
        speak(response)
