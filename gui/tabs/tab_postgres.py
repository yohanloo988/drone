from tkinter import messagebox
import customtkinter as ctk
import config
from gui.components.map_window import FenetreCarte
import psycopg2
from psycopg2 import sql


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
        label_info.pack(pady=(20, 10))

        # 1. Bouton Carte
        btn_map = ctk.CTkButton(
            self,
            text="Prévisualiser la trajectoire sur la carte",
            font=ctk.CTkFont(size=13, weight="bold"),
            height=38,
            width=280,
            command=self.run_map
        )
        btn_map.pack(pady=10)

        # 2. Sélection du Télépilote (Label + ComboBox élargie)
        label_pilot = ctk.CTkLabel(
            self,
            text="Télépilote de la mission :",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        label_pilot.pack(pady=(20, 5))

        pilots_list = getattr(config, 'DJI_PILOT_NAMES', ["Télépilote non défini"])

        self.combo_pilot = ctk.CTkComboBox(
            master=self,
            values=pilots_list,
            width=200,
            height=35,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.combo_pilot.pack(pady=(0, 20))
        if pilots_list:
            self.combo_pilot.set(pilots_list[0])

        # 3. Bouton d'export PostgreSQL
        btn_pg = ctk.CTkButton(
            self,
            text="Charger les données sur Geoserver",
            font=ctk.CTkFont(size=13, weight="bold"),
            height=38,
            width=280,
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
        table_name = getattr(self.app_ref, 'table', None)
        if not table_name:
            messagebox.showwarning("Attention", "Aucune table PostgreSQL n'a été spécifiée.")
            return

        # Récupération du télépilote sélectionné dans l'IHM
        telepilote_selectionne = self.combo_pilot.get()

        self.logger(f"Connexion à la base PostGIS {config.DB_NAME}...")
        self.logger(f"Télépilote sélectionné : {telepilote_selectionne}")

        # Construction dynamique sécurisée avec insertion du champ telepilote
        query = sql.SQL("INSERT INTO {table} (telepilote) VALUES (%s)").format(
            table=sql.Identifier(table_name)
        )

        try:
            with psycopg2.connect(
                    database=config.DB_NAME,
                    user=config.DB_USER,
                    password=config.DB_PASSWORD,
                    host=config.DB_HOST,
                    port=config.DB_PORT
            ) as conn:
                with conn.cursor() as cur:
                    # Le paramètre %s empêche tout problème d'injection SQL
                    cur.execute(query, (telepilote_selectionne,))

            self.logger(f"Insertion réussie dans la table {table_name}.")
            messagebox.showinfo("Succès",
                                f"Données insérées avec succès pour {telepilote_selectionne} dans {table_name} !")

        except psycopg2.Error as e:
            self.logger(f"Erreur PostgreSQL : {e}")
            messagebox.showerror("Erreur Base de Données", f"Échec de l'insertion :\n{e}")
        except Exception as e:
            self.logger(f"Erreur système : {e}")
            messagebox.showerror("Erreur", str(e))