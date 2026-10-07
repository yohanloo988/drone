from tkinter import messagebox
import customtkinter as ctk
from gui.components.map_window import FenetreCarte


class TabPostgres(ctk.CTkFrame):
    def __init__(self, parent, logger, app_ref):
        super().__init__(parent)
        self.logger = logger
        self.app_ref = app_ref
        self.build_ui()

    def build_ui(self):
        label_info = ctk.CTkLabel(
            self,
            text="Module d'export GEOSERVEUR / PostgreSQL (En chantier)",
            font=ctk.CTkFont(size=13, slant="italic")
        )
        label_info.pack(pady=20)

        btn_map = ctk.CTkButton(
            self,
            text="Prévisualiser la trajectoire sur la carte",
            font=ctk.CTkFont(size=13, weight="bold"),
            height=38,
            command=self.run_map
        )
        btn_map.pack(pady=10)

        btn_pg = ctk.CTkButton(
            self,
            text="Charger les données sur Geoserver",
            font=ctk.CTkFont(size=13, weight="bold"),
            height=38,
            fg_color="#D35B58",
            hover_color="#C73E3A",
            command=self.run_pg
        )
        btn_pg.pack(pady=10)

    def run_map(self):
        coords = getattr(self.app_ref, 'coordinate_list', None)
        if not coords:
            messagebox.showwarning("Données manquantes", "Aucune donnée GPS chargée. Exécutez d'abord l'Onglet 2.")
            return

        map_win = FenetreCarte(self)
        map_win.map_widget.set_path(coords, color="blue", width=3)
        premier, dernier = coords[0], coords[-1]
        map_win.map_widget.set_position(premier[0], premier[1])
        map_win.map_widget.set_zoom(16)
        map_win.ajouter_marqueur(premier[0], premier[1], "Décollage")
        map_win.ajouter_marqueur(dernier[0], dernier[1], "Atterrissage")
        self.logger(f"Trajectoire de vol affichée ({len(coords)} points).")

    def run_pg(self):
        messagebox.showinfo("Module en chantier", "Fonctionnalité en cours de développement.")