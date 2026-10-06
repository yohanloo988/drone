import tkinter as tk
from tkinter import ttk, messagebox
from gui.components.log_console import LogConsole
from gui.tabs.tab_txt_json import TabTxtJson
from gui.tabs.tab_json_csv import TabJsonCsv
from gui.tabs.tab_exif_csv import TabExifCsv
from gui.tabs.tab_synthese import TabSynthese
from gui.tabs.tab_postgres import TabPostgres

class DroneToolApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Traitement de données DJI")
        self.geometry("900x650")

        self.style = ttk.Style(self)
        self.style.theme_use("vista")

        self.coordinate_list = []

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)

        self.console = LogConsole(self)

        # Instanciation des onglets
        self.tab_txt_json = TabTxtJson(self.notebook, self.console.log)
        self.tab_json_csv = TabJsonCsv(self.notebook, self.console.log, self)
        self.tab_exif_csv = TabExifCsv(self.notebook, self.console.log)
        self.tab_synthese = TabSynthese(self.notebook, self.console.log)
        self.tab_postgres = TabPostgres(self.notebook, self.console.log, self)

        self.notebook.add(self.tab_txt_json, text="1. TXT ➔ JSON")
        self.notebook.add(self.tab_json_csv, text="2. JSON ➔ CSV")
        self.notebook.add(self.tab_exif_csv, text="3. EXIF Photos ➔ CSV")
        self.notebook.add(self.tab_synthese, text="4. Synthèse")
        self.notebook.add(self.tab_postgres, text="5. CSV ➔ GEOSERVEUR (En chantier)")

        self.build_menu()

    def build_menu(self):
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        menu_aide = tk.Menu(menu_bar, tearoff=0)
        menu_aide.add_command(label="À propos", command=self.afficher_a_propos)
        menu_aide.add_command(label="Documentation", command=self.documentation)
        menu_bar.add_cascade(label="Aide", menu=menu_aide)

    def afficher_a_propos(self):
        messagebox.showinfo("À propos", "Traitement des données DJI - v1.0\nAuteur : Yohan LOO - DITTT")

    def documentation(self):
        messagebox.showinfo("Documentation", "https://docs.google.com/document/d/1Kwup5Q3wRzPn8oXIEMro-Y9O-TEpVaOni70hxHsqa98/edit?usp=sharing")