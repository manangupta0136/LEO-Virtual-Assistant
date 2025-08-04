import tkinter as tk
from tkinter import scrolledtext
from threading import Thread

class LEO_GUI:
    def __init__(self, root, start_leo_callback):
        self.root = root
        self.root.title("LEO - Your AI Assistant")
        self.root.geometry("500x500")
        self.root.config(bg="#121212")

        self.label = tk.Label(root, text="LEO - AI Assistant", font=("Helvetica", 18, "bold"), bg="#121212", fg="white")
        self.label.pack(pady=10)

        self.status_label = tk.Label(root, text="Status: Idle", font=("Helvetica", 12), bg="#121212", fg="lightgray")
        self.status_label.pack()

        self.voice_input = tk.Label(root, text="You said:", font=("Helvetica", 12), bg="#121212", fg="white")
        self.voice_input.pack(pady=5)
        self.user_text = tk.Label(root, text="", wraplength=400, bg="#121212", fg="#00ffcc")
        self.user_text.pack()

        self.response_label = tk.Label(root, text="LEO says:", font=("Helvetica", 12), bg="#121212", fg="white")
        self.response_label.pack(pady=5)
        self.response_text = tk.Label(root, text="", wraplength=400, bg="#121212", fg="#ffaa00")
        self.response_text.pack()

        self.speak_var = tk.BooleanVar(value=True)
        self.speak_checkbox = tk.Checkbutton(root, text="Speak response", variable=self.speak_var, bg="#121212", fg="white", selectcolor="#121212", activebackground="#121212")
        self.speak_checkbox.pack(pady=10)

        self.start_button = tk.Button(root, text="Start LEO", command=lambda: self.start_leo_thread(start_leo_callback), bg="#00ffcc", fg="black")
        self.start_button.pack(pady=10)

        self.quit_button = tk.Button(root, text="Quit", command=self.root.destroy, bg="red", fg="white")
        self.quit_button.pack(pady=10)

    def start_leo_thread(self, callback):
        Thread(target=callback, args=(self,), daemon=True).start()

    def update_status(self, status):
        self.status_label.config(text=f"Status: {status}")

    def update_user_input(self, text):
        self.user_text.config(text=text)

    def update_response(self, text):
        self.response_text.config(text=text)

    def should_speak(self):
        return self.speak_var.get()
