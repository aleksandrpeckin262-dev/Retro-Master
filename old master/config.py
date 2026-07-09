import os

# --- Настройки графического интерфейса (Tkinter) ---
WINDOW_TITLE = "old master"
WINDOW_GEOMETRY = "400x300"
COLOR_BG_TEAL = "#008080"
COLOR_BTN_BG = "#4FC7DB"
COLOR_BTN_ACTIVE = "#006363"
FONT_INTERFACE = ("Arial", 13)

# --- Пути к ресурсам ---
ICON_PATH = r'D:\old master\icon.ico'
BASE_DIR = os.getcwd()

# Путь к картинке градиента для GUI Windows XP
PATH_IMAGE_XP = os.path.join(BASE_DIR, "bg_xp.png")

FOLDER_BG_NOW = os.path.join(BASE_DIR, "bacground_now")
FOLDER_BG_OLD = os.path.join(BASE_DIR, "bacground_old")
FOLDER_CUR_NOW = os.path.join(BASE_DIR, "cursor_now")
FOLDER_CUR_OLD = os.path.join(BASE_DIR, "cursor_old")
FOLDER_SOUNDS_NOW = os.path.join(BASE_DIR, "sounds_now")
FOLDER_ICO_NOW = os.path.join(BASE_DIR, "icons_now")
FOLDER_ICO_OLD = os.path.join(BASE_DIR, "icons_old")

# --- Системные звуки ---
SOUND_START = "win95_start.wav"
SOUND_CLOSE = "win95_close.wav"

# --- Список системных курсоров для полной замены ---
CURSOR_NAMES = ["Arrow", "Help", "AppStarting", "Wait", "IBeam"]

# --- Команды для быстрой перезагрузки оболочки Windows ---
CMD_KILL_EXPLORER = "taskkill /f /im explorer.exe"
CMD_START_EXPLORER = "start explorer"

# --- Волшебные числа Windows API (Константы) ---
SPI_SETDESKWALLPAPER = 20
SPI_SETCURSORS = 87
SPI_SETFONTSMOOTHING = 0x004B
SPI_FLAGS_IMMEDIATE = 0x01 | 0x02

SMOOTHING_OFF_VAL = "0"
SMOOTHING_OFF_TYPE = 0
SMOOTHING_ON_VAL = "2"
SMOOTHING_ON_TYPE = 2

HWND_BROADCAST = 0xFFFF
WM_SETTINGCHANGE = 0x001A
SPI_GETANIMATION = 0x0048
SPI_SETANIMATION = 0x0049

# --- Системные ключи реестра для иконок ---
REG_PATH_COMP_ICON = r"Software\Microsoft\Windows\CurrentVersion\Explorer\CLSID\{20D04FE0-3AEA-1069-A2D8-08002B30309D}\DefaultIcon"
REG_PATH_TRASH_ICON = r"Software\Microsoft\Windows\CurrentVersion\Explorer\CLSID\{645FF040-5081-101B-9F08-00AA002F954E}\DefaultIcon"
