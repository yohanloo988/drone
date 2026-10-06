import pandas as pd
import numpy as np
from pathlib import Path
from core.geo import haversine_distance

def calculer_synthese_photos_vols(log_csv: str, exif_csv: str) -> tuple[str, int, int]:
    """Exécute la jointure temporelle asof entre le log de vol et les EXIF photo."""
    df_log = pd.read_csv(log_csv, low_memory=False)
    df_exif = pd.read_csv(exif_csv, low_memory=False)

    col_time_log = "custom.dateTime" if "custom.dateTime" in df_log.columns else next(
        (c for c in df_log.columns if "datetime" in c.lower() or "time" in c.lower()), None
    )
    col_time_exif = "DateTimeOriginal" if "DateTimeOriginal" in df_exif.columns else "DateTime" if "DateTime" in df_exif.columns else next(
        (c for c in df_exif.columns if "datetime" in c.lower() or "date" in c.lower()), None
    )

    if not col_time_log or not col_time_exif:
        raise ValueError("Colonnes de date/heure introuvables dans les CSV.")

    df_exif['dt_merge'] = pd.to_datetime(df_exif[col_time_exif], format='%Y:%m:%d %H:%M:%S', errors='coerce')
    if df_exif['dt_merge'].isna().all():
        df_exif['dt_merge'] = pd.to_datetime(df_exif[col_time_exif], errors='coerce')

    df_log['dt_utc'] = pd.to_datetime(df_log[col_time_log], format='ISO8601', errors='coerce')
    df_log['dt_merge'] = df_log['dt_utc'].dt.tz_convert('Pacific/Noumea').dt.tz_localize(None)

    df_exif = df_exif.dropna(subset=['dt_merge']).sort_values('dt_merge')
    df_log = df_log.dropna(subset=['dt_merge']).sort_values('dt_merge')
    df_log = df_log[df_log['dt_merge'].dt.year > 2020]

    df_synthese = pd.merge_asof(
        df_exif, df_log, on='dt_merge', direction='nearest', suffixes=('_exif', '_log')
    ).copy()

    if 'dt_utc' in df_synthese.columns:
        dt_log_real = df_synthese['dt_utc'].dt.tz_convert('Pacific/Noumea').dt.tz_localize(None)
        df_synthese['Ecart_Temps_Sec'] = (df_synthese['dt_merge'] - dt_log_real).dt.total_seconds().abs().round(2)
    else:
        df_synthese['Ecart_Temps_Sec'] = np.nan

    if all(col in df_synthese.columns for col in ['GPS_Latitude', 'GPS_Longitude', 'osd.latitude', 'osd.longitude']):
        df_synthese['Ecart_Distance_m'] = haversine_distance(
            df_synthese['GPS_Latitude'], df_synthese['GPS_Longitude'],
            df_synthese['osd.latitude'], df_synthese['osd.longitude']
        ).round(2)
    else:
        df_synthese['Ecart_Distance_m'] = np.nan

    SEUIL_TOLERANCE_SEC = 3.0
    mask_hors_couverture = (df_synthese['Ecart_Temps_Sec'] > SEUIL_TOLERANCE_SEC).fillna(True)
    cols_propres_log = [c for c in df_log.columns if c not in ['dt_merge', 'dt_utc']]

    for c in cols_propres_log:
        if c in df_synthese.columns:
            df_synthese[c] = df_synthese[c].astype(object)

    df_synthese.loc[mask_hors_couverture, cols_propres_log] = np.nan

    COLONNES_CONSERVEES = [
        'FileName', 'dt_merge', 'Ecart_Temps_Sec', 'Ecart_Distance_m',
        'GPS_Latitude', 'GPS_Longitude', 'FNumber', 'ExposureTime', 'ISOSpeedRatings',
        'FocalLength', 'DJI_AbsoluteAltitude', 'DJI_RelativeAltitude', 'DJI_GimbalPitch',
        'osd.flyTime', 'osd.latitude', 'osd.longitude', 'osd.height', 'osd.altitude',
        'osd.pitch', 'osd.roll', 'osd.yaw', 'gimbal.pitch', 'gimbal.roll', 'gimbal.yaw',
        'osd.gpsNum', 'osd.gpsLevel', 'camera.isPhoto', 'home.latitude', 'home.longitude', 'details.aircraftSn'
    ]

    cols_disponibles = [col for col in COLONNES_CONSERVEES if col in df_synthese.columns]
    df_synthese_filtre = df_synthese[cols_disponibles]

    output_dir = Path(exif_csv).parent
    out_synthese = str(output_dir / "synthese_photos_vols.csv")
    df_synthese_filtre.to_csv(out_synthese, index=False, encoding="utf-8-sig")

    nb_couverts = int((~mask_hors_couverture).sum())
    total_photos = len(df_synthese)

    return out_synthese, nb_couverts, total_photos