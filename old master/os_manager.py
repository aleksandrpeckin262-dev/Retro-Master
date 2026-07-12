import ctypes
import os
import winreg
import winsound
import time
import config

class WindowsManager:
    def get_cursor_file_by_name(self, folder_path, cursor_name):
        """Ищет в папке файл, начинающийся на имя курсора (например, arrow_win98)"""
        if not os.path.exists(folder_path): return None
        for f in os.listdir(folder_path):
            if f.lower().startswith(cursor_name.lower()) and os.path.isfile(os.path.join(folder_path, f)):
                return os.path.abspath(os.path.join(folder_path, f))
        return None

    def set_wallpaper(self, path):
        """Меняет обои рабочего стола через WinAPI"""
        if path and os.path.exists(path):
            ctypes.windll.user32.SystemParametersInfoW(config.SPI_SETDESKWALLPAPER, 0, path, config.SPI_FLAGS_IMMEDIATE)

    def set_all_cursors_direct(self, folder_path, is_reset=False):
        """Меняет курсоры по прямому пути к папке"""
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Cursors", 0, winreg.KEY_SET_VALUE)
        for name in config.CURSOR_NAMES:
            if is_reset:
                sys_cur = os.path.join(r"C:\Windows\Cursors", f"aero_{name.lower()}.cur")
                if not os.path.exists(sys_cur): sys_cur = os.path.join(r"C:\Windows\Cursors", f"{name.lower()}.cur")
                winreg.SetValueEx(key, name, 0, winreg.REG_SZ, sys_cur if os.path.exists(sys_cur) else "")
            else:
                cur_file = self.get_cursor_file_by_name(folder_path, name)
                if cur_file: winreg.SetValueEx(key, name, 0, winreg.REG_SZ, cur_file)
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
        """Глобально подменяет Segoe UI на нужный шрифт во всей системе (HKLM)"""
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\FontSubstitutes", 0, winreg.KEY_SET_VALUE)
            if target_font: winreg.SetValueEx(key, "Segoe UI", 0, winreg.REG_SZ, target_font)
            else:
                try: winreg.DeleteValue(key, "Segoe UI")
                except FileNotFoundError: pass
            winreg.CloseKey(key)
            ctypes.windll.user32.SendMessageW(config.HWND_BROADCAST, config.WM_SETTINGCHANGE, 0, "Registry::String")
        except PermissionError:
            print("[Ядро] Нет прав Администратора для изменения глобальных шрифтов HKLM!")

    def set_retro_colors_win32(self, version_name="win95", enable=True):
        """Безопасно перекрашивает классические Win32 элементы окон"""
        elements = list((15, 2, 10, 5, 27))
        if enable:
            if version_name == "win98": colors = list((0x00D4D0C8, 0x00800000, 0x00D4D0C8, 0x00FFFFFF, 0x00A6CAF0))
            else: colors = list((0x00D4D0C8, 0x00800000, 0x00D4D0C8, 0x00FFFFFF, 0x00800000))
        else: colors = list((0x00F0F0F0, 0x00D77800, 0x00B4B4B4, 0x00FFFFFF, 0x00D77800))
        ctypes.windll.user32.SetSysColors(len(elements), (ctypes.c_int * len(elements))(*elements), (ctypes.c_uint * len(colors))(*colors))

    def set_retro_taskbar_color(self, enable=True):
        """Включает серый ретро-цвет панели задач или сбрасывает в родной черный цвет Windows 10"""
        try:
            theme_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(theme_key, "SystemUsesLightTheme", 0, winreg.REG_DWORD, 0)
            if enable: winreg.SetValueEx(theme_key, "ColorPrevalence", 0, winreg.REG_DWORD, 1)
            else: winreg.SetValueEx(theme_key, "ColorPrevalence", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(theme_key)

            dwm_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\DWM", 0, winreg.KEY_SET_VALUE)
            if enable:
                winreg.SetValueEx(dwm_key, "AccentColor", 0, winreg.REG_DWORD, 0x00C8D0D4)
                winreg.SetValueEx(dwm_key, "AccentColorInactive", 0, winreg.REG_DWORD, 0x00C8D0D4)
            else:
                try:
                    winreg.DeleteValue(dwm_key, "AccentColor")
                    winreg.DeleteValue(dwm_key, "AccentColorInactive")
                except FileNotFoundError: pass
            winreg.CloseKey(dwm_key)
        except Exception as e:
            print(f"[Ядро] Ошибка покраски панели: {e}")

    def set_explorer_click_sound_direct(self, path, enable=True):
        """Включает или выключает щелчок Проводника по прямому пути к файлу"""
        try:
            click_key_path = r"AppEvents\Schemes\Apps\Explorer\Navigating\.current"
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, click_key_path, 0, winreg.KEY_SET_VALUE)
            if enable and path and os.path.exists(path):
                winreg.SetValueEx(key, "", 0, winreg.REG_SZ, path)
            else:
                winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "")
            winreg.CloseKey(key)
        except Exception as e:
            print(f"[Ядро] Ошибка настройки звука Проводника: {e}")

    def set_system_icons_direct(self, comp_path, empty_trash_path, full_trash_path, is_reset=False):
        """Заменяет системные иконки по прямым путям к файлам"""
        try:
            comp_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, config.REG_PATH_COMP_ICON)
            if is_reset: winreg.SetValueEx(comp_key, "", 0, winreg.REG_SZ, r"imageres.dll,-109")
            elif comp_path and os.path.exists(comp_path): winreg.SetValueEx(comp_key, "", 0, winreg.REG_SZ, comp_path)
            winreg.CloseKey(comp_key)

            trash_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, config.REG_PATH_TRASH_ICON)
            if is_reset:
                winreg.SetValueEx(trash_key, "", 0, winreg.REG_SZ, r"imageres.dll,-55")
                winreg.SetValueEx(trash_key, "empty", 0, winreg.REG_SZ, r"imageres.dll,-55")
                winreg.SetValueEx(trash_key, "full", 0, winreg.REG_SZ, r"imageres.dll,-54")
            else:
                if empty_trash_path and os.path.exists(empty_trash_path):
                    winreg.SetValueEx(trash_key, "", 0, winreg.REG_SZ, empty_trash_path)
                    winreg.SetValueEx(trash_key, "empty", 0, winreg.REG_SZ, empty_trash_path)
                if full_trash_path and os.path.exists(full_trash_path):
                    winreg.SetValueEx(trash_key, "full", 0, winreg.REG_SZ, full_trash_path)
            winreg.CloseKey(trash_key)
            ctypes.windll.shell32.SHChangeNotify(0x08000000, 0x1000, None, None)
        except Exception as e:
            print(f"[Ядро] Ошибка при обновлении иконок: {e}")

    def play_sound_direct(self, path):
        """Проигрывает .wav файл по прямому пути"""
        if path and os.path.exists(path):
            winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)

    def restart_shell(self):
        """Чистый, безопасный и последовательный перезапуск Проводника Windows 10"""
        try:
            time.sleep(0.3)
            os.system(config.CMD_KILL_EXPLORER)
            time.sleep(0.2)
            os.system(config.CMD_START_EXPLORER)
            ctypes.windll.shell32.SHChangeNotify(0x08000000, 0x1000, None, None)
            print("[Ядро] Оболочка успешно перезапущена.")
        except Exception as e:
            print(f"[Ядро] Ошибка перезапуска оболочки: {e}")
