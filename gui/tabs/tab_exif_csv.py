import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from io_services.exif_parser import extraire_exif_dossier

class TabExifCsv(ttk.Frame):
    def __init__(self, parent, logger):
        super().__init__(parent, padding=15)
        self.logger = logger
        self.build_ui()

    def build_ui(self):
        ttk.Label(self, text="Dossier des photos PVA :").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_photos_dir = ttk.Entry(self, width=100)
        self.entry_photos_dir.grid(row=0, column=1, padx=5)
        ttk.Button(self, text="Parcourir...", command=self.browse_photos_dir).grid(row=0, column=2)

        ttk.Button(self, text="Extraire EXIF / XMP ➔ CSV", command=self.run_thread).grid(row=1, column=1, pady=20)

    def browse_photos_dir(self):
        if d := filedialog.askdirectory():
            self.entry_photos_dir.delete(0, tk.END)
            self.entry_photos_dir.insert(0, d)

    def run_thread(self):
        threading.Thread(target=self.run_action, daemon=True).start()

    def run_action(self):
        folder = self.entry_photos_dir.get()
        if not folder:
            messagebox.showwarning("Attention", "Sélectionnez un dossier de photos.")
            return

        self.logger(f"Analyse des métadonnées du dossier : {folder}")
        try:
            out_csv = extraire_exif_dossier(folder, logger=self.logger)
            self.logger(f"Terminé ! CSV généré : {out_csv}")
            messagebox.showinfo("Succès", f"Métadonnées exportées :\n{out_csv}")
        except Exception as e:
            self.logger(f"Erreur EXIF ➔ CSV : {e}")
            messagebox.showerror("Erreur", str(e))