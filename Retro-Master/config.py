import os

# Настройки GUI
WINDOW_TITLE = "Retro master"
WINDOW_GEOMETRY = "400x300"
COLOR_BG_TEAL = "#008080"
COLOR_BTN_BG = "#4FC7DB"
COLOR_BTN_ACTIVE = "#006363"
FONT_INTERFACE = ("Arial", 13)

# Базовые каталоги 
ICON_PATH = r'C:\Retro-Master\icon.ico'
BASE_DIR = os.getcwd()
PATH_IMAGE_XP = os.path.join(BASE_DIR, "bg_xp.png")

# Пути к файлам
THEME_RESOURCES = {
    "win95": {
        "wallpaper": r"C:\Retro-Master\bacground_now\bacground_now_win95\win95_wallpaper.jpg",                        # рабочий стол
        "sound_start": r"C:\Retro-Master\sounds_now\sounds_win95\start_win95\start_win95.wav",                        # запуск win95
        "sound_close": r"C:\Retro-Master\sounds_now\sounds_win95\close_win95\close_win95.wav",                        # выход win95
        "icon_computer": r"C:\Retro-Master\icons_now\icon_win95\computer_win95\computer_win95.ico",                   # иконка ПК
        "icon_trash_empty": r"C:\Retro-Master\icons_now\icon_win95\trash_empty_win95\trash_empty_win95.ico",          # иконка пустой корзины
        "icon_trash_full": r"C:\Retro-Master\icons_now\icon_win95\trash_full_win95\trash_full_win95.ico",             # иконка полной корзины
        "cursors_dir": r"C:\Retro-Master\cursor_now\win95_cur"                                                        # Папка, где лежат курсоры 95
    },
    "win98": {
        "wallpaper": r"C:\Retro-Master\bacground_now\bacground_now_win98\win98_wallpaper.jpg",                        # рабочий стол
        "sound_start": r"C:\Retro-Master\sounds_now\sounds_win98\start_win98\start_win98.wav",                        # запуск win98
        "sound_close": r"C:\Retro-Master\sounds_now\sounds_win98\close_win98\close_win98.wav",                        # выход win98
        "sound_click": r"C:\Retro-Master\sounds_now\sounds_win98\click_win98\click_win98.wav",                        # звук клика
        "icon_computer": r"C:\Retro-Master\icons_now\icon_win98\computer_win98\computer_win98.ico",                   # иконка ПК
        "icon_trash_empty": r"C:\Retro-Master\icons_now\icon_win98\trash_empty_win98\trash_empty_win98.ico",          # иконка пустой корзины
        "icon_trash_full": r"C:\Retro-Master\icons_now\icon_win98\trash_full_win98\trash_full_win98.ico",             # иконка полной корзины
        "cursors_dir": r"C:\Retro-Master\cursor_now\win98_cur"                                                        # Папка, где лежат курсоры 98
    },
    "winXP": {
        "wallpaper": r"C:\Retro-Master\bacground_now\bacground_now_winXP\winXP_wallpaper.jpg",                        # рабочий стол
        "sound_start": r"C:\Retro-Master\sounds_now\sounds_winXP\start_winXP\start_winXP.wav",                        # запуск winXP
        "sound_close": r"C:\Retro-Master\sounds_now\sounds_winXP\close_winXP\close_winXP.wav",                        # выход winXP
        "icon_computer": r"C:\Retro-Master\icons_now\computer_winXP\computer_winXP.ico",                              # иконка ПК
        "icon_trash_empty": r"C:\Retro-Master\icons_now\icon_winXP\trash_empty_winXP\trash_empty_winXP.ico",          # иконка пустой корзины
        "icon_trash_full": r"C:\Retro-Master\icons_now\icon_winXP\trash_full_winXP\trash_full_winXP.ico",             # иконка полной корзины
        "cursors_dir": r"C:\Retro-Master\cursor_now\winXP_cur"                                                        # Папка, где лежат курсоры XP
    },
    "vista": {
        "wallpaper": r"C:\Retro-Master\bacground_now\bacground_now_winVista\winVista_wallpaper.jpg",                  # рабочий стол
        "sound_start": r"C:\Retro-Master\sounds_now\sounds_winVista\start_winVista\start_winVista.wav",               # запуск winVista
        "sound_close": r"C:\Retro-Master\sounds_now\sounds_winVista\close_winVista\close_winVista.wav",               # выход winVista
        "icon_computer": r"C:\Retro-Master\icons_now\icon_winVista\computer_winVista\computer_winVista.ico",          # иконка ПК
        "icon_trash_empty": r"C:\Retro-Master\icons_now\icon_winVista\trash_empty_winVista\trash_empty_winVista.ico", # иконка пустой корзины
        "icon_trash_full": r"C:\Retro-Master\icons_now\icon_winVista\trash_full_winVista\trash_full_winVista.ico",    # иконка полной корзины
        "cursors_dir": r"C:\Retro-Master\cursor_now\winVista_cur"                                                     # Папка, где лежат курсоры Vista
    },
    "win7": {
        "wallpaper": r"C:\Retro-Master\bacground_now\bacground_now_win7\win7_wallpaper.jpg",                          # рабочий стол
        "sound_start": r"C:\Retro-Master\sounds_now\sounds_win7\start_win7\start_win7.wav",                           # запуск win7
        "sound_close": r"C:\Retro-Master\sounds_now\sounds_win7\close_win7\close_win7.wav",                           # выход win7
        "icon_computer": r"C:\Retro-Master\icons_now\icon_win7\computer_win7\computer_win7.ico",                      # иконка ПК
        "icon_trash_empty": r"C:\Retro-Master\icons_now\icon_win7\trash_empty_win7\trash_empty_win7.ico",             # иконка пустой корзины
        "icon_trash_full": r"C:\Retro-Master\icons_now\icon_win7\trash_full_win7\trash_full_win7.ico",                # иконка полной корзины
        "cursors_dir": r"C:\Retro-Master\cursor_now\win7_cur"                                                         # Папка, где лежат курсоры 7
    },
    # Пути для отката
    "restore": {
        "wallpaper": r"C:\Retro-Master\bacground_old\default_wallpaper.jpg",                                          # дефолтные обои
        "cursors_old_dir": r"C:\Retro-Master\cursors_old",                                                            # старый курсор
        "icons_old_dir": r"C:\Retro-Master\icons_old"                                                                 # старые иконки
    }
}

# Названия курсоров и системные константы
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
