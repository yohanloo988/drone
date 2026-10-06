from tkinter import ttk, messagebox
from gui.components.map_window import FenetreCarte

class TabPostgres(ttk.Frame):
    def __init__(self, parent, logger, app_ref):
        super().__init__(parent, padding=15)
        self.logger = logger
        self.app_ref = app_ref
        self.build_ui()

    def build_ui(self):
        ttk.Label(self, text="Module en cours de conception...").pack(pady=10)
        ttk.Button(self, text="Prévisualiser les données", command=self.run_map).pack(pady=20)
        ttk.Button(self, text="Charger les données sur Geoserveur", command=self.run_pg).pack(pady=20)

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
        pass