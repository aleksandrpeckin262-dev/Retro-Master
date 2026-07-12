import os

# --- Настройки графического интерфейса (Tkinter) ---
WINDOW_TITLE = "old master"
WINDOW_GEOMETRY = "400x300"
COLOR_BG_TEAL = "#008080"
COLOR_BTN_BG = "#4FC7DB"
COLOR_BTN_ACTIVE = "#006363"
FONT_INTERFACE = ("Arial", 13)

# --- Базовые каталоги ---
ICON_PATH = r'D:\old master\icon.ico'
BASE_DIR = os.getcwd()
PATH_IMAGE_XP = os.path.join(BASE_DIR, "bg_xp.png")

# --- БАНК ПУТЕЙ ДЛЯ ВСЕХ ВЕРСИЙ WINDOWS ---
# Здесь прописываются прямые пути к конкретным файлам для каждой ОС
THEME_RESOURCES = {
    "win95": {
        "wallpaper": r"D:\old master\bacground_now\bacground_now_win95\win95_wallpaper.png", # Укажите ваше точное имя файла
        "sound_start": r"D:\old master\sounds_now\start_win95.wav",
        "icon_computer": r"D:\old master\icons_now\computer_win95.ico",
        "icon_trash_empty": r"D:\old master\icons_now\trash_empty_win95.ico",
        "icon_trash_full": r"D:\old master\icons_now\trash_full_win95.ico",
        "cursors_dir": r"D:\old master\cursor_now\win95_cur" # Папка, где лежат курсоры 95-й
    },
    "win98": {
        "wallpaper": r"D:\old master\bacground_now\bacground_now_win98\win98_wallpaper.png", # Укажите ваше точное имя файла
        "sound_start": r"D:\old master\sounds_now\start_win98.wav",
        "sound_click": r"D:\old master\sounds_now\click.wav",
        "icon_computer": r"D:\old master\icons_now\computer_win98.ico",
        "icon_trash_empty": r"D:\old master\icons_now\trash_empty_win98.ico",
        "icon_trash_full": r"D:\old master\icons_now\trash_full_win98.ico",
        "cursors_dir": r"D:\old master\cursor_now\win98_cur"
    },
    "winXP": {
        "wallpaper": r"D:\old master\bacground_now\bacground_now_winXP\winXP_wallpaper.png",
        "sound_start": r"D:\old master\sounds_now\start_winXP.wav",
        "icon_computer": r"D:\old master\icons_now\computer_winXP.ico",
        "icon_trash_empty": r"D:\old master\icons_now\trash_empty_winXP.ico",
        "icon_trash_full": r"D:\old master\icons_now\trash_full_winXP.ico",
        "cursors_dir": r"D:\old master\cursor_now\winXP_cur"
    },
    "vista": {
        "wallpaper": r"D:\old master\bacground_now\bacground_now_winVista\vista_wallpaper.png",
        "sound_start": r"D:\old master\sounds_now\start_vista.wav",
        "icon_computer": r"D:\old master\icons_now\computer_vista.ico",
        "icon_trash_empty": r"D:\old master\icons_now\trash_empty_vista.ico",
        "icon_trash_full": r"D:\old master\icons_now\trash_full_vista.ico",
        "cursors_dir": r"D:\old master\cursor_now\winVista_cur"
    },
    "win7": {
        "wallpaper": r"D:\old master\bacground_now\bacground_now_win7\win7_wallpaper.png",
        "sound_start": r"D:\old master\sounds_now\start_win7.wav",
        "icon_computer": r"D:\old master\icons_now\computer_win7.ico",
        "icon_trash_empty": r"D:\old master\icons_now\trash_empty_win7.ico",
        "icon_trash_full": r"D:\old master\icons_now\trash_full_win7.ico",
        "cursors_dir": r"D:\old master\cursor_now\win7_cur"
    },
    # Пути для отката к стандартной Windows 10
    "restore": {
        "wallpaper": r"D:\old master\bacground_old\default_wallpaper.jpg", # Ваши старые дефолтные обои
        "sound_close": r"D:\old master\sounds_now\close_win95.wav",
        "cursors_old_dir": r"D:\old master\cursors_old",
        "icons_old_dir": r"D:\old master\icons_old"
    }
}

# --- Названия курсоров и системные константы ---
CURSOR_NAMES = ["Arrow", "Help", "AppStarting", "Wait", "IBeam"]
CMD_KILL_EXPLORER = "taskkill /f /im explorer.exe"
CMD_START_EXPLORER = "start explorer"

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

REG_PATH_COMP_ICON = r"Software\Microsoft\Windows\CurrentVersion\Explorer\CLSID\{20D04FE0-3AEA-1069-A2D8-08002B30309D}\DefaultIcon"
REG_PATH_TRASH_ICON = r"Software\Microsoft\Windows\CurrentVersion\Explorer\CLSID\{645FF040-5081-101B-9F08-00AA002F954E}\DefaultIcon"