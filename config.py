# config.py

# API KEY du compte DJI Developer (https://developer.dji.com) attribuée à yohan.loo@gouv.nc
DJI_API_KEY = "f0191f17893654d9043731d7cd3abd7" # SDK Type : Open API

# ------Outil de conversion txt->JSON : dji-log-x86_64-pc-windows-msvc.zip v0.57 ------#
# ------------ Source GIT : https://github.com/lvauvillier/dji-log-parser/ ------------#
DEFAULT_EXE_PATH = r"C:\Users\yohan.loo\PycharmProjects\drone\data\dji-log-x86_64-pc-windows-msvc\dji-log.exe"

# PostgreSQL credentials
DB_HOST = ""
DB_PORT = 5432
DB_NAME = ""
DB_USER = ""
DB_PASSWORD = ""
DB_SCHEMA = ""

# PostgreSQL : filtrage des colonnes
DB_FILTERED_FIELDS = []