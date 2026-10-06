import tkinter as tk
from tkinter import ttk

class LogConsole(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text=" Console de suivi ")
        self.pack(fill="both", expand=True, padx=10, pady=5)

        self.log_text = tk.Text(self, height=8, state="disabled", bg="#1e1e1e", fg="#00ff00", font=("Consolas", 9))
        self.log_text.pack(fill="both", expand=True, padx=5, pady=5)

    def log(self, message: str):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, f"> {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")