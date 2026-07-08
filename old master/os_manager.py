import ctypes
import os
import winreg
import winsound
import time
import config

class WindowsManager:
    def __init__(self):
        self.sounds_dir = config.FOLDER_SOUNDS_NOW

    def get_first_file(self, folder_name):
        """Ищет первый файл в указанной папке внутри каталога проекта"""
        folder_path = os.path.join(config.BASE_DIR, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            return None
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        # Фикс: используем .pop(0) для безопасного вытаскивания первой строки без квадратных скобок
        return os.path.abspath(os.path.join(folder_path, files.pop(0))) if files else None

    def get_specific_file(self, folder_name, file_name):
        """Ищет файл с конкретным именем в указанной папке ресурсов"""
        folder_path = os.path.join(config.BASE_DIR, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            return None
        target_path = os.path.join(folder_path, file_name)
        return os.path.abspath(target_path) if os.path.exists(target_path) else None

    def get_cursor_file(self, folder_path, cursor_name):
        """Ищет конкретный курсор по его имени в папке ресурсов"""
        if not os.path.exists(folder_path):
            return None
        for f in os.listdir(folder_path):
            if f.lower().startswith(cursor_name.lower()) and os.path.isfile(os.path.join(folder_path, f)):
                return os.path.abspath(os.path.join(folder_path, f))
        return None

    def set_wallpaper(self, path):
        """Меняет обои рабочего стола через WinAPI"""
        if path:
            ctypes.windll.user32.SystemParametersInfoW(config.SPI_SETDESKWALLPAPER, 0, path, config.SPI_FLAGS_IMMEDIATE)

    def set_all_cursors(self, folder_path, is_reset=False):
        """Меняет или сбрасывает весь пак основных курсоров"""
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Cursors", 0, winreg.KEY_SET_VALUE)
        for name in config.CURSOR_NAMES:
            if is_reset:
                sys_cur = os.path.join(r"C:\Windows\Cursors", f"aero_{name.lower()}.cur")
                if not os.path.exists(sys_cur):
                    sys_cur = os.path.join(r"C:\Windows\Cursors", f"{name.lower()}.cur")
                winreg.SetValueEx(key, name, 0, winreg.REG_SZ, sys_cur if os.path.exists(sys_cur) else "")
            else:
                cur_file = self.get_cursor_file(folder_path, name)
                if cur_file:
                    winreg.SetValueEx(key, name, 0, winreg.REG_SZ, cur_file)
        winreg.CloseKey(key)
        ctypes.windll.user32.SystemParametersInfoW(config.SPI_SETCURSORS, 0, 0, config.SPI_FLAGS_IMMEDIATE)

    def set_clear_type(self, enable=True):
        """Включает или выключает сглаживание шрифтов ClearType"""
        ctypes.windll.user32.SystemParametersInfoW(config.SPI_SETFONTSMOOTHING, enable, 0, config.SPI_FLAGS_IMMEDIATE)
        smoothing_val = config.SMOOTHING_ON_VAL if enable else config.SMOOTHING_OFF_VAL
        smoothing_type = config.SMOOTHING_ON_TYPE if enable else config.SMOOTHING_OFF_TYPE
        
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "FontSmoothing", 0, winreg.REG_SZ, smoothing_val)
        winreg.SetValueEx(key, "FontSmoothingType", 0, winreg.REG_DWORD, smoothing_type)
        winreg.CloseKey(key)

    def set_global_font_substitute(self, target_font):
        """Глобально подменяет Segoe UI на нужный шрифт во всей системе (HKLM). Требует админа!"""
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\FontSubstitutes", 0, winreg.KEY_SET_VALUE)
            if target_font:
                winreg.SetValueEx(key, "Segoe UI", 0, winreg.REG_SZ, target_font)
            else:
                try: winreg.DeleteValue(key, "Segoe UI")
                except FileNotFoundError: pass
            winreg.CloseKey(key)
            ctypes.windll.user32.SendMessageW(config.HWND_BROADCAST, config.WM_SETTINGCHANGE, 0, "Registry::String")
        except PermissionError:
            print("[Ядро] Нет прав Администратора для изменения глобальных шрифтов HKLM!")

    def set_retro_colors_win32(self, version_name="win95", enable=True):
        """Безопасно перекрашивает классические Win32 элементы через SetSysColors"""
        # Индексы системных элементов: 15=ButtonFace, 2=ActiveCaption, 10=ActiveBorder, 5=Window, 27=GradientActiveCaption
        elements = [15, 2, 10, 5, 27]
        
        if enable:
            if version_name == "win98":
                # Каноничный градиент Windows 98: темно-синий переходит в голубой
                colors = [0x00D4D0C8, 0x00800000, 0x00D4D0C8, 0x00FFFFFF, 0x00A6CAF0]
            else:
                # Windows 95: сплошной синий цвет (оба цвета заголовка одинаковые)
                colors = [0x00D4D0C8, 0x00800000, 0x00D4D0C8, 0x00FFFFFF, 0x00800000]
        else:
            # Дефолтные цвета Windows 10
            colors = [0x00F0F0F0, 0x00D77800, 0x00B4B4B4, 0x00FFFFFF, 0x00D77800]
            
        ctypes.windll.user32.SetSysColors(len(elements), (ctypes.c_int * len(elements))(*elements), (ctypes.c_uint * len(colors))(*colors))

    def set_retro_taskbar_color(self, enable=True):
        """Включает серый ретро-цвет или сбрасывает его в родной черный цвет Windows 10"""
        try:
            theme_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize", 0, winreg.KEY_SET_VALUE)
            
            # Всегда держим SystemUsesLightTheme = 0 (Темный режим Windows 10)
            # Это заставит панель задач становиться канонично ЧЕРНОЙ при ресете.
            winreg.SetValueEx(theme_key, "SystemUsesLightTheme", 0, winreg.REG_DWORD, 0)
            
            if enable:
                winreg.SetValueEx(theme_key, "ColorPrevalence", 0, winreg.REG_DWORD, 1)
            else:
                winreg.SetValueEx(theme_key, "ColorPrevalence", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(theme_key)

            dwm_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\DWM", 0, winreg.KEY_SET_VALUE)
            if enable:
                winreg.SetValueEx(dwm_key, "AccentColor", 0, winreg.REG_DWORD, 0x00C8D0D4) # Серый (ABGR)
                winreg.SetValueEx(dwm_key, "AccentColorInactive", 0, winreg.REG_DWORD, 0x00C8D0D4)
            winreg.CloseKey(dwm_key)
            print("[Ядро] Параметры цвета панели задач успешно исправлены.")
        except Exception as e:
            print(f"[Ядро] Ошибка покраски панели: {e}")

    def set_system_icons(self, is_reset=False):
        """Заменяет системные иконки Рабочего стола и принудительно сбрасывает их кэш"""
        try:
            comp_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, config.REG_PATH_COMP_ICON)
            if is_reset:
                winreg.SetValueEx(comp_key, "", 0, winreg.REG_SZ, r"imageres.dll,-109")
            else:
                comp_ico = self.get_specific_file("icons_now", "computer.ico")
                if comp_ico: winreg.SetValueEx(comp_key, "", 0, winreg.REG_SZ, comp_ico)
            winreg.CloseKey(comp_key)

            trash_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, config.REG_PATH_TRASH_ICON)
            if is_reset:
                winreg.SetValueEx(trash_key, "", 0, winreg.REG_SZ, r"imageres.dll,-55")
                winreg.SetValueEx(trash_key, "empty", 0, winreg.REG_SZ, r"imageres.dll,-55")
                winreg.SetValueEx(trash_key, "full", 0, winreg.REG_SZ, r"imageres.dll,-54")
            else:
                t_empty = self.get_specific_file("icons_now", "trash_empty.ico")
                t_full = self.get_specific_file("icons_now", "trash_full.ico")
                if t_empty:
                    winreg.SetValueEx(trash_key, "", 0, winreg.REG_SZ, t_empty)
                    winreg.SetValueEx(trash_key, "empty", 0, winreg.REG_SZ, t_empty)
                if t_full: winreg.SetValueEx(trash_key, "full", 0, winreg.REG_SZ, t_full)
            winreg.CloseKey(trash_key)

            ctypes.windll.shell32.SHChangeNotify(0x08000000, 0x1000, None, None)
            print("[Ядро] Системные иконки обновлены.")
        except Exception as e:
            print(f"[Ядро] Ошибка при обновлении иконок: {e}")

    def play_sound(self, filename):
        """Проигрывает .wav файл из папки ресурсов в асинхронном фоновом режиме"""
        wav_path = os.path.join(self.sounds_dir, filename)
        if os.path.exists(wav_path):
            winsound.PlaySound(wav_path, winsound.SND_FILENAME | winsound.SND_ASYNC)

    def restart_shell(self):
        """Мгновенно перезапускает Проводник и жестко очищает графический кэш Рабочего стола"""
        try:
            time.sleep(0.3) # Даем Windows 300мс зафиксировать цвет хотбара в реестре DWM
            os.system(config.CMD_KILL_EXPLORER)
            class ANIMATIONINFO(ctypes.Structure):
                _fields_ = [("cbSize", ctypes.c_uint), ("iMinAnimate", ctypes.c_int)]
            anim_info = ANIMATIONINFO()
            anim_info.cbSize = ctypes.sizeof(ANIMATIONINFO)
            ctypes.windll.user32.SystemParametersInfoW(config.SPI_GETANIMATION, anim_info.cbSize, ctypes.byref(anim_info), 0)
            ctypes.windll.user32.SystemParametersInfoW(config.SPI_SETANIMATION, anim_info.cbSize, ctypes.byref(anim_info), config.SPI_FLAGS_IMMEDIATE)
            os.system(config.CMD_START_EXPLORER)
            print("Оболочка и кэш Рабочего стола успешно обновлены!")
        except Exception as e:
            print(f"Ошибка перезапуска оболочки: {e}")

