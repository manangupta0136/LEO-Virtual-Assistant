# gui.py

import tkinter as tk
from tkinter import scrolledtext
from threading import Thread

class LEO_GUI:
    def __init__(self, root, start_leo_callback):
        self.root = root
        self.root.title("LEO - Your AI Assistant")
        self.root.geometry("500x600")  # Increased height for chat window
        self.root.config(bg="#121212")

        # --- Title and Status ---
        self.title_label = tk.Label(root, text="LEO - AI Assistant", font=("Helvetica", 18, "bold"), bg="#121212", fg="white")
        self.title_label.pack(pady=10)

        self.status_label = tk.Label(root, text="Status: Idle", font=("Helvetica", 12), bg="#121212", fg="lightgray")
        self.status_label.pack(pady=5)

        # --- Chat Window ---
        self.chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg="#1e1e1e", fg="white", font=("Helvetica", 11), state='disabled')
        self.chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Configure tags for user and LEO text colors
        self.chat_window.tag_config('user', foreground='#00ffcc') # Your color
        self.chat_window.tag_config('leo', foreground='#ffaa00')  # LEO's color

        # --- Controls ---
        controls_frame = tk.Frame(root, bg="#121212")
        controls_frame.pack(fill=tk.X, padx=10, pady=5)

        self.speak_var = tk.BooleanVar(value=True)
        self.speak_checkbox = tk.Checkbutton(controls_frame, text="Speak response", variable=self.speak_var, bg="#121212", fg="white", selectcolor="#1e1e1e", activebackground="#121212", relief=tk.FLAT)
        self.speak_checkbox.pack(side=tk.LEFT, padx=10)

        self.start_button = tk.Button(controls_frame, text="Start LEO", command=lambda: self.start_leo_thread(start_leo_callback), bg="#00ffcc", fg="black", relief=tk.FLAT)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.quit_button = tk.Button(controls_frame, text="Quit", command=self.root.destroy, bg="#ff4b5c", fg="white", relief=tk.FLAT)
        self.quit_button.pack(side=tk.RIGHT, padx=10)

    def start_leo_thread(self, callback):
        self.start_button.config(state=tk.DISABLED, text="Running...")
        Thread(target=callback, args=(self,), daemon=True).start()

    def add_to_chat_window(self, sender: str, message: str):
        """Adds a message to the chat window with appropriate styling."""
        self.chat_window.config(state='normal') # Enable writing
        
        sender_tag = 'user' if sender.lower() == 'you' else 'leo'
        self.chat_window.insert(tk.END, f"{sender}: ", (sender_tag, 'bold'))
        self.chat_window.insert(tk.END, f"{message}\n\n")
        
        self.chat_window.config(state='disabled') # Disable writing
        self.chat_window.see(tk.END) # Auto-scroll to the bottom

    def update_status(self, status):
        self.status_label.config(text=f"Status: {status}")

    def should_speak(self):
        return self.speak_var.get()