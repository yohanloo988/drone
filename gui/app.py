import customtkinter as ctk
from tkinter import messagebox

# Configuration du thème global
ctk.set_appearance_mode("system")  # "System", "Dark", "Light"
ctk.set_default_color_theme("dark-blue") # "blue", "dark-blue", "green"

from gui.components.log_console import LogConsole
from gui.tabs.tab_txt_json import TabTxtJson
from gui.tabs.tab_json_csv import TabJsonCsv
from gui.tabs.tab_exif_csv import TabExifCsv
from gui.tabs.tab_synthese import TabSynthese
from gui.tabs.tab_postgres import TabPostgres


class DroneToolApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Traitement de données DJI - Modern UI")
        self.geometry("950x700")

        self.coordinate_list = []

        # Conteneur d'onglets CustomTkinter
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=5)

        # Création des onglets
        self.tab_txt = self.tabview.add("1. TXT ➔ JSON")
        self.tab_json = self.tabview.add("2. JSON ➔ CSV")
        self.tab_exif = self.tabview.add("3. EXIF Photos ➔ CSV")
        self.tab_syn = self.tabview.add("4. Synthèse")
        self.tab_pg = self.tabview.add("5. GEOSERVEUR")

        # Console de logs
        self.console = LogConsole(self)

        # Instanciation de nos frames dans les onglets
        self.view_txt = TabTxtJson(self.tab_txt, self.console.log)
        self.view_txt.pack(fill="both", expand=True)

        self.view_json = TabJsonCsv(self.tab_json, self.console.log, self)
        self.view_json.pack(fill="both", expand=True)

        self.view_exif = TabExifCsv(self.tab_exif, self.console.log)
        self.view_exif.pack(fill="both", expand=True)

        self.view_synthese = TabSynthese(self.tab_syn, self.console.log)
        self.view_synthese.pack(fill="both", expand=True)

        self.view_postgres = TabPostgres(self.tab_pg, self.console.log, self)
        self.view_postgres.pack(fill="both", expand=True)