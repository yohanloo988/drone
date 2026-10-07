import customtkinter as ctk


class LogConsole(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True, padx=10, pady=5)

        # Label d'en-tête de la console
        self.label_title = ctk.CTkLabel(
            self,
            text="Console de suivi",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        self.label_title.pack(fill="x", padx=10, pady=(5, 0))

        # Zone de texte défilante pour les logs
        self.log_text = ctk.CTkTextbox(
            self,
            height=120,
            font=ctk.CTkFont(family="Consolas", size=12),
            text_color="#00FF00",
            fg_color="#1E1E1E"
        )
        self.log_text.pack(fill="both", expand=True, padx=10, pady=5)
        self.log_text.configure(state="disabled")

    def log(self, message: str):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"> {message}\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")