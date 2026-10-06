import numpy as np

def convert_gps_to_degrees(gps_coords, ref):
    if not gps_coords or not ref:
        return None
    try:
        deg = float(gps_coords[0])
        minute = float(gps_coords[1])
        sec = float(gps_coords[2])
        dec = deg + (minute / 60.0) + (sec / 3600.0)
        if ref in ['S', 'W']:
            dec = -dec
        return dec
    except Exception:
        return str(gps_coords)

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calcule la distance en mètres entre deux points GPS."""
    R = 6371000.0  # Rayon de la Terre en mètres
    phi1, phi2 = np.radians(lat1), np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlambda = np.radians(lon2 - lon1)

    a = np.sin(dphi / 2.0) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlambda / 2.0) ** 2
    return 2 * R * np.arctan2(np.sqrt(a), np.sqrt(1.0 - a))