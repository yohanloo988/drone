import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from io_services.log_converter import convertir_json_vers_csv

class TabJsonCsv(ttk.Frame):
    def __init__(self, parent, logger, app_ref):
        super().__init__(parent, padding=15)
        self.logger = logger
        self.app_ref = app_ref
        self.build_ui()

    def build_ui(self):
        ttk.Label(self, text="Fichier JSON à aplatir :").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_json = ttk.Entry(self, width=100)
        self.entry_json.grid(row=0, column=1, padx=5)
        ttk.Button(self, text="Parcourir...", command=self.browse_json).grid(row=0, column=2)

        ttk.Button(self, text="Générer le CSV des Frames", command=self.run_thread).grid(row=1, column=1, pady=20)

    def browse_json(self):
        if f := filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")]):
            self.entry_json.delete(0, tk.END)
            self.entry_json.insert(0, f)

    def run_thread(self):
        threading.Thread(target=self.run_action, daemon=True).start()

    def run_action(self):
        json_path = self.entry_json.get()
        if not json_path:
            messagebox.showwarning("Attention", "Sélectionnez un fichier JSON.")
            return

        try:
            self.logger("Lecture du JSON et extraction des frames...")
            out_csv, coords = convertir_json_vers_csv(json_path)
            self.app_ref.coordinate_list = coords
            self.logger(f"{len(coords)} points GPS valides extraits.")
            self.logger(f"CSV généré : {out_csv}")
            messagebox.showinfo("Succès", f"Fichier CSV créé :\n{out_csv}")
        except Exception as e:
            self.logger(f"Erreur JSON ➔ CSV : {e}")
            messagebox.showerror("Erreur", str(e))