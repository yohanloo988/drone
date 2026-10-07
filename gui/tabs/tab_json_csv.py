import threading
from tkinter import filedialog, messagebox
import customtkinter as ctk
from io_services.log_converter import convertir_json_vers_csv


class TabJsonCsv(ctk.CTkFrame):
    def __init__(self, parent, logger, app_ref):
        super().__init__(parent)
        self.logger = logger
        self.app_ref = app_ref
        self.build_ui()

    def build_ui(self):
        self.grid_columnconfigure(1, weight=1)

        label_json = ctk.CTkLabel(self, text="Fichier JSON à aplatir :", anchor="w")
        label_json.grid(row=0, column=0, padx=15, pady=15, sticky="w")

        self.entry_json = ctk.CTkEntry(self, placeholder_text="Sélectionner le fichier .json")
        self.entry_json.grid(row=0, column=1, padx=10, pady=15, sticky="ew")

        btn_browse = ctk.CTkButton(self, text="Parcourir...", width=110, command=self.browse_json)
        btn_browse.grid(row=0, column=2, padx=15, pady=15)

        btn_convert = ctk.CTkButton(
            self,
            text="Générer le CSV des Frames",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            fg_color="#1f538d",
            hover_color="#14375e",
            command=self.run_thread
        )
        btn_convert.grid(row=1, column=1, pady=30)

    def browse_json(self):
        if f := filedialog.askopenfilename(filetypes=[("Fichiers JSON", "*.json")]):
            self.entry_json.delete(0, "end")
            self.entry_json.insert(0, f)

    def run_thread(self):
        threading.Thread(target=self.run_action, daemon=True).start()

    def run_action(self):
        json_path = self.entry_json.get()
        if not json_path:
            messagebox.showwarning("Attention", "Veuillez sélectionner un fichier JSON.")
            return

        try:
            self.logger("Lecture du JSON et extraction des frames...")
            out_csv, coords = convertir_json_vers_csv(json_path)
            self.app_ref.coordinate_list = coords
            self.logger(f"{len(coords)} points GPS valides extraits.")
            self.logger(f"CSV généré : {out_csv}")
            messagebox.showinfo("Succès", f"Fichier CSV créé :\n{out_csv}")
        except Exception as e:
            self.logger(f"Erreur JSON ➔ CSV : {e}")
            messagebox.showerror("Erreur", str(e))