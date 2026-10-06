import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import config
from io_services.log_converter import convertir_txt_vers_json

class TabTxtJson(ttk.Frame):
    def __init__(self, parent, logger):
        super().__init__(parent, padding=15)
        self.logger = logger
        self.build_ui()

    def build_ui(self):
        ttk.Label(self, text="Exécutable Parser (.exe) :").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_exe = ttk.Entry(self, width=100)
        self.entry_exe.grid(row=0, column=1, padx=5)
        if hasattr(config, 'DEFAULT_EXE_PATH'):
            self.entry_exe.insert(0, config.DEFAULT_EXE_PATH)
        ttk.Button(self, text="Parcourir...", command=self.browse_exe).grid(row=0, column=2)

        ttk.Label(self, text="Fichier Log DJI (.txt) :").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_txt = ttk.Entry(self, width=100)
        self.entry_txt.grid(row=1, column=1, padx=5)
        ttk.Button(self, text="Parcourir...", command=self.browse_txt).grid(row=1, column=2)

        ttk.Label(self, text="Clé d'API DJI Developer :").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_api = ttk.Entry(self, width=100)
        self.entry_api.grid(row=2, column=1, padx=5)
        if hasattr(config, 'DJI_API_KEY'):
            self.entry_api.insert(0, config.DJI_API_KEY)

        ttk.Button(self, text="Convertir en JSON", command=self.run_thread).grid(row=4, column=1, pady=20)

    def browse_exe(self):
        if f := filedialog.askopenfilename(filetypes=[("Exécutables Windows", "*.exe")]):
            self.entry_exe.delete(0, tk.END)
            self.entry_exe.insert(0, f)

    def browse_txt(self):
        if f := filedialog.askopenfilename(filetypes=[("Logs TXT DJI", "*.txt")]):
            self.entry_txt.delete(0, tk.END)
            self.entry_txt.insert(0, f)

    def run_thread(self):
        threading.Thread(target=self.run_action, daemon=True).start()

    def run_action(self):
        exe, txt, api = self.entry_exe.get(), self.entry_txt.get(), self.entry_api.get()
        if not exe or not txt:
            messagebox.showwarning("Attention", "Spécifiez l'exécutable et le fichier TXT.")
            return

        self.logger("Lancement de la conversion TXT ➔ JSON...")
        try:
            out_json = convertir_txt_vers_json(exe, txt, api)
            self.logger(f"Succès ! Fichier JSON généré : {out_json}")
            messagebox.showinfo("Succès", f"Fichier JSON généré :\n{out_json}")
        except Exception as e:
            self.logger(f"Erreur : {e}")
            messagebox.showerror("Erreur", str(e))