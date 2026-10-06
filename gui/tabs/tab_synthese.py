import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from core.processing import calculer_synthese_photos_vols

class TabSynthese(ttk.Frame):
    def __init__(self, parent, logger):
        super().__init__(parent, padding=15)
        self.logger = logger
        self.build_ui()

    def build_ui(self):
        ttk.Label(self, text="Fichier CSV Log de vol :").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_csv_log = ttk.Entry(self, width=80)
        self.entry_csv_log.grid(row=0, column=1, padx=5)
        ttk.Button(self, text="Parcourir...", command=self.browse_csv_log).grid(row=0, column=2)

        ttk.Label(self, text="Fichier CSV Métadonnées Photos :").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_csv_exif = ttk.Entry(self, width=80)
        self.entry_csv_exif.grid(row=1, column=1, padx=5)
        ttk.Button(self, text="Parcourir...", command=self.browse_csv_exif).grid(row=1, column=2)

        ttk.Button(self, text="Générer la Synthèse (Jointure & CQ)", command=self.run_thread).grid(row=2, column=1, pady=20)

    def browse_csv_log(self):
        if f := filedialog.askopenfilename(filetypes=[("Fichiers CSV", "*.csv")]):
            self.entry_csv_log.delete(0, tk.END)
            self.entry_csv_log.insert(0, f)

    def browse_csv_exif(self):
        if f := filedialog.askopenfilename(filetypes=[("Fichiers CSV", "*.csv")]):
            self.entry_csv_exif.delete(0, tk.END)
            self.entry_csv_exif.insert(0, f)

    def run_thread(self):
        threading.Thread(target=self.run_action, daemon=True).start()

    def run_action(self):
        log_csv, exif_csv = self.entry_csv_log.get(), self.entry_csv_exif.get()
        if not log_csv or not exif_csv:
            messagebox.showwarning("Attention", "Veuillez sélectionner les deux fichiers CSV.")
            return

        try:
            self.logger("Calcul de la synthèse en cours...")
            out_file, nb_couverts, total = calculer_synthese_photos_vols(log_csv, exif_csv)
            self.logger(f"Synthèse terminée : {nb_couverts}/{total} photos couvertes.")
            self.logger(f"Fichier généré : {out_file}")
            messagebox.showinfo("Succès", f"Synthèse créée avec succès !\n\nPhotos couvertes : {nb_couverts}/{total}\n\nFichier :\n{out_file}")
        except Exception as e:
            self.logger(f"Erreur Synthèse : {e}")
            messagebox.showerror("Erreur", str(e))