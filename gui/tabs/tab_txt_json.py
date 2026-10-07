import threading
from tkinter import filedialog, messagebox
import customtkinter as ctk
import config
from io_services.log_converter import convertir_txt_vers_json


class TabTxtJson(ctk.CTkFrame):
    def __init__(self, parent, logger):
        super().__init__(parent)
        self.logger = logger
        self.build_ui()

    def build_ui(self):
        # Configuration des colonnes pour un redimensionnement propre
        self.grid_columnconfigure(1, weight=1)

        # 1. Sélection de l'exécutable
        label_exe = ctk.CTkLabel(self, text="Exécutable Parser (.exe) :", anchor="w")
        label_exe.grid(row=0, column=0, padx=15, pady=10, sticky="w")

        self.entry_exe = ctk.CTkEntry(self, placeholder_text="Chemin vers dji-log.exe")
        self.entry_exe.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        if hasattr(config, 'DEFAULT_EXE_PATH'):
            self.entry_exe.insert(0, config.DEFAULT_EXE_PATH)

        btn_browse_exe = ctk.CTkButton(self, text="Parcourir...", width=110, command=self.browse_exe)
        btn_browse_exe.grid(row=0, column=2, padx=15, pady=10)

        # 2. Sélection du fichier TXT
        label_txt = ctk.CTkLabel(self, text="Fichier Log DJI (.txt) :", anchor="w")
        label_txt.grid(row=1, column=0, padx=15, pady=10, sticky="w")

        self.entry_txt = ctk.CTkEntry(self, placeholder_text="Sélectionner le fichier .txt")
        self.entry_txt.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        btn_browse_txt = ctk.CTkButton(self, text="Parcourir...", width=110, command=self.browse_txt)
        btn_browse_txt.grid(row=1, column=2, padx=15, pady=10)

        # 3. Clé d'API DJI Developer
        label_api = ctk.CTkLabel(self, text="Clé d'API DJI Developer :", anchor="w")
        label_api.grid(row=2, column=0, padx=15, pady=10, sticky="w")

        self.entry_api = ctk.CTkEntry(self, placeholder_text="Clé API DJI (Optionnelle selon la version)")
        self.entry_api.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        if hasattr(config, 'DJI_API_KEY'):
            self.entry_api.insert(0, config.DJI_API_KEY)

        # 4. Bouton d'action principal
        self.btn_convert = ctk.CTkButton(
            self,
            text="Convertir en JSON",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            fg_color="#1f538d",
            hover_color="#14375e",
            command=self.run_thread
        )
        self.btn_convert.grid(row=3, column=1, pady=30)

    def browse_exe(self):
        f = filedialog.askopenfilename(filetypes=[("Exécutables Windows", "*.exe")])
        if f:
            self.entry_exe.delete(0, "end")
            self.entry_exe.insert(0, f)

    def browse_txt(self):
        f = filedialog.askopenfilename(filetypes=[("Logs TXT DJI", "*.txt")])
        if f:
            self.entry_txt.delete(0, "end")
            self.entry_txt.insert(0, f)

    def run_thread(self):
        threading.Thread(target=self.run_action, daemon=True).start()

    def run_action(self):
        exe, txt, api = self.entry_exe.get(), self.entry_txt.get(), self.entry_api.get()
        if not exe or not txt:
            messagebox.showwarning("Attention", "Veuillez spécifier l'exécutable et le fichier TXT.")
            return

        self.logger("Lancement de la conversion TXT ➔ JSON...")
        try:
            out_json = convertir_txt_vers_json(exe, txt, api)
            self.logger(f"Succès ! Fichier JSON généré : {out_json}")
            messagebox.showinfo("Succès", f"Fichier JSON généré :\n{out_json}")
        except Exception as e:
            self.logger(f"Erreur : {e}")
            messagebox.showerror("Erreur", str(e))