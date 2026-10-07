import threading
from tkinter import filedialog, messagebox
import customtkinter as ctk
from io_services.exif_parser import extraire_exif_dossier


class TabExifCsv(ctk.CTkFrame):
    def __init__(self, parent, logger):
        super().__init__(parent)
        self.logger = logger
        self.build_ui()

    def build_ui(self):
        self.grid_columnconfigure(1, weight=1)

        label_photos = ctk.CTkLabel(self, text="Dossier des photos PVA :", anchor="w")
        label_photos.grid(row=0, column=0, padx=15, pady=15, sticky="w")

        self.entry_photos_dir = ctk.CTkEntry(self, placeholder_text="Sélectionner le répertoire contenant les photos JPG")
        self.entry_photos_dir.grid(row=0, column=1, padx=10, pady=15, sticky="ew")

        btn_browse = ctk.CTkButton(self, text="Parcourir...", width=110, command=self.browse_photos_dir)
        btn_browse.grid(row=0, column=2, padx=15, pady=15)

        btn_extract = ctk.CTkButton(
            self,
            text="Extraire EXIF / XMP ➔ CSV",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            fg_color="#1f538d",
            hover_color="#14375e",
            command=self.run_thread
        )
        btn_extract.grid(row=1, column=1, pady=30)

    def browse_photos_dir(self):
        if d := filedialog.askdirectory():
            self.entry_photos_dir.delete(0, "end")
            self.entry_photos_dir.insert(0, d)

    def run_thread(self):
        threading.Thread(target=self.run_action, daemon=True).start()

    def run_action(self):
        folder = self.entry_photos_dir.get()
        if not folder:
            messagebox.showwarning("Attention", "Veuillez sélectionner un dossier de photos.")
            return

        self.logger(f"Analyse des métadonnées du dossier : {folder}")
        try:
            out_csv = extraire_exif_dossier(folder, logger=self.logger)
            self.logger(f"Terminé ! CSV généré : {out_csv}")
            messagebox.showinfo("Succès", f"Métadonnées exportées :\n{out_csv}")
        except Exception as e:
            self.logger(f"Erreur EXIF ➔ CSV : {e}")
            messagebox.showerror("Erreur", str(e))