import json
import subprocess
from pathlib import Path
import pandas as pd

def convertir_txt_vers_json(exe_path: str, txt_path: str, api_key: str) -> str:
    out_json = str(Path(txt_path).with_suffix('.json'))
    cmd = [exe_path, "--api-key", api_key, "--output", out_json, txt_path]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    _, stderr = process.communicate()

    if process.returncode != 0:
        raise RuntimeError(f"Erreur dji-log : {stderr}")

    return out_json

def convertir_json_vers_csv(json_path: str) -> tuple[str, list[tuple[float, float]]]:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    df_frames = pd.json_normalize(data["frames"])

    if "details" in data and isinstance(data["details"], dict):
        df_details = pd.json_normalize(data["details"]).add_prefix("details.")
        for col in df_details.columns:
            df_frames[col] = df_details[col].iloc[0]

    coordinate_list = []
    if "osd.latitude" in df_frames.columns and "osd.longitude" in df_frames.columns:
        df_gps = df_frames[(df_frames["osd.latitude"] != 0) & (df_frames["osd.longitude"] != 0)]
        coordinate_list = list(zip(df_gps["osd.latitude"], df_gps["osd.longitude"]))

    out_csv = str(Path(json_path).with_suffix('.csv'))
    df_frames.to_csv(out_csv, index=False, encoding="utf-8-sig")

    return out_csv, coordinate_list