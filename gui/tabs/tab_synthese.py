import threading
from tkinter import filedialog, messagebox
import customtkinter as ctk
from core.processing import calculer_synthese_photos_vols


class TabSynthese(ctk.CTkFrame):
    def __init__(self, parent, logger):
        super().__init__(parent)
        self.logger = logger
        self.build_ui()

    def build_ui(self):
        self.grid_columnconfigure(1, weight=1)

        # 1. CSV Log de vol
        label_log = ctk.CTkLabel(self, text="Fichier CSV Log de vol :", anchor="w")
        label_log.grid(row=0, column=0, padx=15, pady=10, sticky="w")

        self.entry_csv_log = ctk.CTkEntry(self, placeholder_text="CSV extrait du log DJI")
        self.entry_csv_log.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        btn_browse_log = ctk.CTkButton(self, text="Parcourir...", width=110, command=self.browse_csv_log)
        btn_browse_log.grid(row=0, column=2, padx=15, pady=10)

        # 2. CSV EXIF Photos
        label_exif = ctk.CTkLabel(self, text="Fichier CSV Photos :", anchor="w")
        label_exif.grid(row=1, column=0, padx=15, pady=10, sticky="w")

        self.entry_csv_exif = ctk.CTkEntry(self, placeholder_text="CSV extrait des EXIF photos")
        self.entry_csv_exif.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        btn_browse_exif = ctk.CTkButton(self, text="Parcourir...", width=110, command=self.browse_csv_exif)
        btn_browse_exif.grid(row=1, column=2, padx=15, pady=10)

        # 3. Action Synthèse
        btn_generate = ctk.CTkButton(
            self,
            text="Générer la Synthèse (Jointure & CQ)",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            fg_color="#2FA572",
            hover_color="#1E6F4C",
            command=self.run_thread
        )
        btn_generate.grid(row=2, column=1, pady=30)

    def browse_csv_log(self):
        if f := filedialog.askopenfilename(filetypes=[("Fichiers CSV", "*.csv")]):
            self.entry_csv_log.delete(0, "end")
            self.entry_csv_log.insert(0, f)

    def browse_csv_exif(self):
        if f := filedialog.askopenfilename(filetypes=[("Fichiers CSV", "*.csv")]):
            self.entry_csv_exif.delete(0, "end")
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