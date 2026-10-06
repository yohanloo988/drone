cd C:\Users\yohan.loo\PycharmProjects\drone

pyinstaller --noconfirm --onedir --windowed --name "DJI_Tool_DITTT" --icon="app_icon.ico" --collect-all tkintermapview --collect-all pandas --collect-all PIL C:\Users\yohan.loo\PycharmProjects\drone\main.py