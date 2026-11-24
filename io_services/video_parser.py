import json
import re
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd

_DOC_KEY_RE = re.compile(r"^Doc(\d+)(?:-(\d+))?$")


def _is_gps_fix(lat: float, lon: float) -> bool:
    return abs(lat) <= 90.0 and abs(lon) <= 180.0 and not (lat == 0.0 and lon == 0.0)


def extraire_telemetrie_video(
    video_path: str | Path,
    exiftool_path: str = "exiftool.exe",
    config_path: str | None = None,
    logger=None
) -> tuple[str, list[tuple[float, float]]]:
    """
    Extrait la télémétrie d'une vidéo (.MP4/.MOV) ou d'un .SRT DJI,
    génère le fichier CSV sans colonnes GPS en double et retourne (chemin_csv, liste_coordonnees).
    """
    path_obj = Path(video_path)

    if path_obj.suffix.lower() == ".srt":
        if logger:
            logger(f"Lecture du fichier sous-titres SRT : {path_obj.name}")
        df = _parse_srt(path_obj)
    else:
        if logger:
            logger(f"Extraction du flux Protobuf via ExifTool : {path_obj.name}")
        df = _parse_mp4_exiftool_complet(path_obj, exiftool_path, config_path)

    if df.empty or "GPSLatitude" not in df.columns or "GPSLongitude" not in df.columns:
        raise ValueError("Aucune donnée GPS valide trouvée dans ce fichier vidéo.")

    out_csv = str(path_obj.with_suffix(".csv"))
    df.to_csv(out_csv, index=False, encoding="utf-8-sig")

    # Extraction des coordonnées valides pour la carte depuis les champs natifs
    df_valid_gps = df.dropna(subset=["GPSLatitude", "GPSLongitude"])
    coords = list(zip(df_valid_gps["GPSLatitude"], df_valid_gps["GPSLongitude"]))

    return out_csv, coords


def _parse_mp4_exiftool_complet(video_path: Path, exiftool_path: str, config_path: str | None) -> pd.DataFrame:
    """Extrait les balises décodées par ExifTool pour chaque trame sans duplication de coordonnées."""
    cmd = [exiftool_path]
    if config_path and Path(config_path).is_file():
        cmd.extend(["-config", str(config_path)])

    cmd.extend([
        "-ee", "-j", "-g3", "-n",
        "-api", "LargeFileSupport=1",
        "-api", "QuickTimeUTC=1",
        str(video_path)
    ])

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    except FileNotFoundError:
        raise FileNotFoundError(f"Exécutable ExifTool introuvable : {exiftool_path}")

    if proc.returncode != 0:
        raise RuntimeError(f"Erreur ExifTool : {proc.stderr.strip()[-300:]}")

    data = json.loads(proc.stdout) if proc.stdout.strip() else []
    if not data:
        return pd.DataFrame()

    root = data[0]

    rows = []
    for key, value in root.items():
        match = _DOC_KEY_RE.match(key)
        if match and isinstance(value, dict):
            row = {"DocIndex": int(match.group(1)), "SubIndex": int(match.group(2) or 0)}
            row.update(value)
            rows.append(row)

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows).sort_values(["DocIndex", "SubIndex"]).reset_index(drop=True)

    # Conversion numérique et filtrage des (0, 0) directement sur GPSLatitude / GPSLongitude
    if "GPSLatitude" in df.columns and "GPSLongitude" in df.columns:
        df["GPSLatitude"] = pd.to_numeric(df["GPSLatitude"], errors="coerce")
        df["GPSLongitude"] = pd.to_numeric(df["GPSLongitude"], errors="coerce")
        mask_fix = df.apply(
            lambda r: _is_gps_fix(r["GPSLatitude"], r["GPSLongitude"]) if pd.notna(r["GPSLatitude"]) and pd.notna(r["GPSLongitude"]) else False,
            axis=1
        )
        df = df[mask_fix].copy()
    else:
        return pd.DataFrame()

    # Conversion horaire UTC -> Nouméa (UTC+11)
    if "GPSDateTime" in df.columns:
        dt_utc = pd.to_datetime(
            df["GPSDateTime"].astype(str).str.rstrip("Z").str.strip(),
            format="%Y:%m:%d %H:%M:%S.%f",
            errors="coerce"
        )
        if dt_utc.isna().all():
            dt_utc = pd.to_datetime(
                df["GPSDateTime"].astype(str).str.rstrip("Z").str.strip(),
                format="%Y:%m:%d %H:%M:%S",
                errors="coerce"
            )
        df["dt_noumea"] = dt_utc + pd.Timedelta(hours=11)

    df.insert(0, "video_file", video_path.name)
    return df


def _parse_srt(srt_path: Path) -> pd.DataFrame:
    """Parse un fichier sous-titres DJI (.SRT) en utilisant les mêmes noms de colonnes GPS."""
    content = srt_path.read_text(encoding="utf-8")
    blocks = content.strip().split("\n\n")
    samples: list[dict] = []
    abs_dt_re = re.compile(r"(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2}):(\d{2})[.,](\d{3})")

    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue
        ts_match = re.search(r"(\d{2}:\d{2}:\d{2},\d{3})", lines[1])
        cue = ts_match.group(1) if ts_match else ""
        tele_line = re.sub(r"<[^>]+>", "", " ".join(lines[2:]))

        dt_local = None
        m_dt = abs_dt_re.search(tele_line)
        if m_dt:
            y, mo, d, h, mi, s, ms = (int(g) for g in m_dt.groups())
            dt_local = datetime(y, mo, d, h, mi, s, ms * 1000)

        lat_m = re.search(r"\[latitude:\s*([+-]?\d+\.?\d*)\]", tele_line)
        lon_m = re.search(r"\[longitude:\s*([+-]?\d+\.?\d*)\]", tele_line)
        alt_m = re.search(r"abs_alt:\s*([+-]?\d+\.?\d*)\]", tele_line)
        rel_m = re.search(r"rel_alt:\s*([+-]?\d+\.?\d*)", tele_line)
        yaw_m = re.search(r"gb_yaw:\s*([+-]?\d+\.?\d*)", tele_line)
        pitch_m = re.search(r"gb_pitch:\s*([+-]?\d+\.?\d*)", tele_line)
        focal_m = re.search(r"\[focal_len\s*:\s*([+-]?\d+\.?\d*)", tele_line)

        if lat_m and lon_m:
            lat, lon = float(lat_m.group(1)), float(lon_m.group(1))
            if not _is_gps_fix(lat, lon):
                continue

            focal_val = float(focal_m.group(1)) if focal_m else None
            if focal_val and focal_val >= 100.0:
                focal_val /= 10.0

            samples.append({
                "video_file": srt_path.name,
                "cue_srt": cue,
                "GPSDateTime": (dt_local - timedelta(hours=11)) if dt_local else None,
                "dt_noumea": dt_local,
                "GPSLatitude": lat,
                "GPSLongitude": lon,
                "AbsoluteAltitude": float(alt_m.group(1)) if alt_m else 0.0,
                "RelativeAltitude": float(rel_m.group(1)) if rel_m else None,
                "GimbalYaw": float(yaw_m.group(1)) if yaw_m else None,
                "GimbalPitch": float(pitch_m.group(1)) if pitch_m else None,
                "FocalLength": focal_val,
            })

    return pd.DataFrame(samples)