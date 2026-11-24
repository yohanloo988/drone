import threading
from tkinter import filedialog, messagebox
import customtkinter as ctk
import config
from io_services.video_parser import extraire_telemetrie_video


class TabVideoCsv(ctk.CTkFrame):
    def __init__(self, parent, logger, app):
        super().__init__(parent)
        self.logger = logger
        self.app = app
        self.build_ui()

    def build_ui(self):
        self.grid_columnconfigure(1, weight=1)

        # Ligne 0 : Exécutable ExifTool
        lbl_exe = ctk.CTkLabel(self, text="Exécutable ExifTool (.exe) :", anchor="w")
        lbl_exe.grid(row=0, column=0, padx=15, pady=15, sticky="w")

        self.entry_exiftool = ctk.CTkEntry(self, placeholder_text="Chemin vers exiftool.exe")
        self.entry_exiftool.grid(row=0, column=1, padx=10, pady=15, sticky="ew")
        if hasattr(config, 'DEFAULT_EXIFTOOL_PATH'):
            self.entry_exiftool.insert(0, config.DEFAULT_EXIFTOOL_PATH)

        btn_browse_exe = ctk.CTkButton(self, text="Parcourir...", width=110, command=self.browse_exiftool)
        btn_browse_exe.grid(row=0, column=2, padx=15, pady=15)

        # Ligne 1 : Fichier Vidéo ou SRT
        lbl_vid = ctk.CTkLabel(self, text="Vidéo (.MP4/.MOV) ou .SRT :", anchor="w")
        lbl_vid.grid(row=1, column=0, padx=15, pady=15, sticky="w")

        self.entry_video = ctk.CTkEntry(self, placeholder_text="Sélectionner une vidéo DJI ou un fichier .SRT")
        self.entry_video.grid(row=1, column=1, padx=10, pady=15, sticky="ew")

        btn_browse_vid = ctk.CTkButton(self, text="Parcourir...", width=110, command=self.browse_video)
        btn_browse_vid.grid(row=1, column=2, padx=15, pady=15)

        # Ligne 2 : Bouton d'action
        btn_extract = ctk.CTkButton(
            self,
            text="Extraire Télémétrie Vidéo ➔ CSV",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            fg_color="#1f538d",
            hover_color="#14375e",
            command=self.run_thread
        )
        btn_extract.grid(row=2, column=1, pady=30)

    def browse_exiftool(self):
        if f := filedialog.askopenfilename(filetypes=[("Exécutables Windows", "*.exe")]):
            self.entry_exiftool.delete(0, "end")
            self.entry_exiftool.insert(0, f)

    def browse_video(self):
        if f := filedialog.askopenfilename(
            filetypes=[("Vidéos & Sous-titres DJI", "*.mp4;*.mov;*.srt"), ("Tous les fichiers", "*.*")]
        ):
            self.entry_video.delete(0, "end")
            self.entry_video.insert(0, f)

    def run_thread(self):
        threading.Thread(target=self.run_action, daemon=True).start()

    def run_action(self):
        video_path = self.entry_video.get()
        exiftool_path = self.entry_exiftool.get() or "exiftool.exe"

        if not video_path:
            messagebox.showwarning("Attention", "Veuillez sélectionner une vidéo ou un fichier .SRT.")
            return

        self.logger(f"Analyse de la télémétrie vidéo : {video_path}")
        try:
            cfg_path = getattr(config, 'EXIFTOOL_CONFIG_PATH', None)
            out_csv, coords = extraire_telemetrie_video(
                video_path,
                exiftool_path=exiftool_path,
                config_path=cfg_path,
                logger=self.logger
            )

            # Alimente la trace GPS de l'application pour la prévisualisation carte
            self.app.coordinate_list = coords

            self.logger(f"Terminé ! {len(coords)} points extraits ➔ {out_csv}")
            messagebox.showinfo(
                "Succès",
                f"Télémétrie vidéo exportée ({len(coords)} points) :\n{out_csv}"
            )
        except Exception as e:
            self.logger(f"Erreur Vidéo ➔ CSV : {e}")
            messagebox.showerror("Erreur", str(e))