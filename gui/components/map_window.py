import tkinter as tk
from tkintermapview import TkinterMapView

class FenetreCarte(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Carte de prévisualisation des vols")
        self.geometry("800x600")

        self.transient(parent)
        self.map_widget = TkinterMapView(self, width=800, height=600, corner_radius=0)
        self.map_widget.pack(fill="both", expand=True)

        fond_gnc = "https://tiles.arcgis.com/tiles/TZcrgU6CIbqWt9Qv/arcgis/rest/services/fond_imagerie/MapServer/tile/{z}/{y}/{x}"
        self.map_widget.set_tile_server(fond_gnc, max_zoom=19)
        self.map_widget.set_position(-21.448, 165.587)
        self.map_widget.set_zoom(7)

    def ajouter_marqueur(self, lat, lon, texte="Point Drone"):
        return self.map_widget.set_marker(lat, lon, text=texte)