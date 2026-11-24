# config.py

# API KEY du compte DJI Developer (https://developer.dji.com) attribuée à yohan.loo@gouv.nc
DJI_API_KEY = "f0191f17893654d9043731d7cd3abd7" # SDK Type : Open API

# ------Outil de conversion txt->JSON : dji-log-x86_64-pc-windows-msvc.zip v0.57 ------#
# ------------ Source GIT : https://github.com/lvauvillier/dji-log-parser/ ------------#
DEFAULT_EXE_PATH = r"C:\Users\yohan.loo\PycharmProjects\drone\data\dji-log-x86_64-pc-windows-msvc\dji-log.exe"

# Liste des télépilotes
DJI_PILOT_NAMES =[
        "Quentin CARDON",
        "Perrine DRAIN",
        "Cyril PINSAT",
        "Mégane HAGUET",
        "Elodie LAUNAY"
]

# PostgreSQL credentials
DB_HOST = ""
DB_PORT = 5432
DB_NAME = ""
DB_USER = ""
DB_PASSWORD = ""
DB_SCHEMA = ""

# PostgreSQL : filtrage des colonnes
# COLONNES_CONSERVEES = [
#         'FileName', 'dt_merge', 'Ecart_Temps_Sec', 'Ecart_Distance_m',
#         'GPS_Latitude', 'GPS_Longitude', 'FNumber', 'ExposureTime', 'ISOSpeedRatings',
#         'FocalLength', 'DJI_AbsoluteAltitude', 'DJI_RelativeAltitude', 'DJI_GimbalPitch',
#         'osd.flyTime', 'osd.latitude', 'osd.longitude', 'osd.height', 'osd.altitude',
#         'osd.pitch', 'osd.roll', 'osd.yaw', 'gimbal.pitch', 'gimbal.roll', 'gimbal.yaw',
#         'osd.gpsNum', 'osd.gpsLevel', 'camera.isPhoto', 'home.latitude', 'home.longitude', 'details.aircraftSn'
#     ]

DEFAULT_EXIFTOOL_PATH = r"C:\Users\yohan.loo\PycharmProjects\drone\utils\exiftool-13.64_64\exiftool-13.64_64\exiftool.exe"
EXIFTOOL_CONFIG_PATH = r"C:\Users\yohan.loo\PycharmProjects\drone\utils\exiftool.config"