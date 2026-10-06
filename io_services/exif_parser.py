import os
from PIL import Image, ExifTags
import pandas as pd
from core.geo import convert_gps_to_degrees

def decode_bytes(val):
    if isinstance(val, bytes):
        try:
            decoded = val.decode("utf-16le").rstrip("\x00")
            if decoded.isprintable():
                return decoded
        except (UnicodeDecodeError, ValueError):
            pass

        for encoding in ["utf-8", "latin-1", "ascii"]:
            try:
                decoded = val.decode(encoding).rstrip("\x00").strip()
                cleaned = "".join(c for c in decoded if c.isprintable())
                if cleaned:
                    return cleaned
            except (UnicodeDecodeError, ValueError):
                pass
        return val.hex()
    return val

def extraire_exif_dossier(folder_path: str, logger=None) -> str:
    photos_data = []
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg'))]

    for i, filename in enumerate(files, 1):
        path_file = os.path.join(folder_path, filename)
        with Image.open(path_file) as img:
            exif_data = img._getexif()
            if exif_data:
                exif = {ExifTags.TAGS[k]: v for k, v in exif_data.items() if k in ExifTags.TAGS}
                exif_cleaned = {k: decode_bytes(v) for k, v in exif.items()}

                if "GPSInfo" in exif:
                    gps_info = exif["GPSInfo"]
                    exif_cleaned["GPS_Latitude"] = convert_gps_to_degrees(gps_info.get(2), gps_info.get(1))
                    exif_cleaned["GPS_Longitude"] = convert_gps_to_degrees(gps_info.get(4), gps_info.get(3))
                    del exif_cleaned["GPSInfo"]

                exif_cleaned["FileName"] = filename
                exif_cleaned["FilePath"] = path_file

                try:
                    xmp_data = img.getxmp()
                    if xmp_data:
                        meta = xmp_data[0].get("Description", {})
                        exif_cleaned["DJI_AbsoluteAltitude"] = meta.get("AbsoluteAltitude")
                        exif_cleaned["DJI_RelativeAltitude"] = meta.get("RelativeAltitude")
                        exif_cleaned["DJI_GimbalPitch"] = meta.get("GimbalPitchDegree")
                except Exception:
                    pass

                photos_data.append(exif_cleaned)

        if logger and i % 20 == 0:
            logger(f"Progression : {i}/{len(files)} photos analysées...")

    df_photos = pd.DataFrame(photos_data)
    out_csv = os.path.join(folder_path, "metadata_photos.csv")
    df_photos.to_csv(out_csv, index=False, encoding="utf-8-sig")
    return out_csv