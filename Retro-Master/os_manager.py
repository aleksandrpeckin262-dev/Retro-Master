import ctypes, os, winreg, winsound, time, subprocess, config

class WindowsManager:
    def get_cursor_file_by_name(self, folder_path, cursor_name):
        if not folder_path or not os.path.exists(folder_path): return None
        try:
            for f in os.listdir(folder_path):
                if f.lower().startswith(cursor_name.lower()) and os.path.isfile(os.path.join(folder_path, f)):
                    return os.path.abspath(os.path.join(folder_path, f))
        except Exception: pass
        return None

    def set_wallpaper(self, path):
        if path and os.path.exists(path):
            ctypes.windll.user32.SystemParametersInfoW(config.SPI_SETDESKWALLPAPER, 0, path, config.SPI_FLAGS_IMMEDIATE)

    def set_all_cursors_direct(self, folder_path, is_reset=False):
        try:
            if not is_reset and (not folder_path or not os.path.exists(folder_path)): return
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
        except Exception as e: print(f"[Ядро] Ошибка курсоров: {e}")

    def set_clear_type(self, enable=True):
        try:
            ctypes.windll.user32.SystemParametersInfoW(config.SPI_SETFONTSMOOTHING, enable, 0, config.SPI_FLAGS_IMMEDIATE)
            smoothing_val = config.SMOOTHING_ON_VAL if enable else config.SMOOTHING_OFF_VAL
            smoothing_type = config.SMOOTHING_ON_TYPE if enable else config.SMOOTHING_OFF_TYPE
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "FontSmoothing", 0, winreg.REG_SZ, smoothing_val)
            winreg.SetValueEx(key, "FontSmoothingType", 0, winreg.REG_DWORD, smoothing_type)
            winreg.CloseKey(key)
        except Exception: pass

    def set_global_font_substitute(self, target_font):
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\FontSubstitutes", 0, winreg.KEY_SET_VALUE)
            if target_font: winreg.SetValueEx(key, "Segoe UI", 0, winreg.REG_SZ, target_font)
            else:
                try: winreg.DeleteValue(key, "Segoe UI")
                except FileNotFoundError: pass
            winreg.CloseKey(key)
            ctypes.windll.user32.SendMessageW(config.HWND_BROADCAST, config.WM_SETTINGCHANGE, 0, "Registry::String")
        except PermissionError: pass

    def set_retro_colors_win32(self, version_name="win95", enable=True):
        try:
            elements = list((15, 2, 10, 5, 27))
            if enable:
                if version_name == "win98": colors = list((0x00D4D0C8, 0x00800000, 0x00D4D0C8, 0x00FFFFFF, 0x00A6CAF0))
                else: colors = list((0x00D4D0C8, 0x00800000, 0x00D4D0C8, 0x00FFFFFF, 0x00800000))
            else: colors = list((0x00F0F0F0, 0x00D77800, 0x00B4B4B4, 0x00FFFFFF, 0x00D77800))
            ctypes.windll.user32.SetSysColors(len(elements), (ctypes.c_int * len(elements))(*elements), (ctypes.c_uint * len(colors))(*colors))
        except Exception: pass

    def set_retro_taskbar_color(self, enable=True):
        try:
            theme_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(theme_key, "SystemUsesLightTheme", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(theme_key, "ColorPrevalence", 0, winreg.REG_DWORD, 1 if enable else 0)
            winreg.CloseKey(theme_key)
            dwm_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\DWM", 0, winreg.KEY_SET_VALUE)
            if enable:
                winreg.SetValueEx(dwm_key, "AccentColor", 0, winreg.REG_DWORD, 0x00C8D0D4)
                winreg.SetValueEx(dwm_key, "AccentColorInactive", 0, winreg.REG_DWORD, 0x00C8D0D4)
            else:
                try: winreg.DeleteValue(dwm_key, "AccentColor"); winreg.DeleteValue(dwm_key, "AccentColorInactive")
                except FileNotFoundError: pass
            winreg.CloseKey(dwm_key)
        except Exception: pass

    def set_explorer_click_sound_direct(self, path, enable=True):
        try:
            click_key_path = r"AppEvents\Schemes\Apps\Explorer\Navigating\.current"
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, click_key_path, 0, winreg.KEY_SET_VALUE)
            if enable and path and os.path.exists(path): winreg.SetValueEx(key, "", 0, winreg.REG_SZ, path)
            else: winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "")
            winreg.CloseKey(key)
        except Exception: pass

    def set_system_icons_direct(self, comp_path, empty_trash_path, full_trash_path, is_reset=False):
        try:
            comp_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, config.REG_PATH_COMP_ICON)
            if is_reset:
                try: winreg.DeleteValue(comp_key, "")
                except FileNotFoundError: pass
            elif comp_path and os.path.exists(comp_path): 
                winreg.SetValueEx(comp_key, "", 0, winreg.REG_SZ, comp_path)
            winreg.CloseKey(comp_key)

            trash_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, config.REG_PATH_TRASH_ICON)
            if is_reset:
                try: winreg.DeleteValue(trash_key, ""); winreg.DeleteValue(trash_key, "empty"); winreg.DeleteValue(trash_key, "full")
                except FileNotFoundError: pass
            else:
                if empty_trash_path and os.path.exists(empty_trash_path):
                    winreg.SetValueEx(trash_key, "", 0, winreg.REG_SZ, empty_trash_path)
                    winreg.SetValueEx(trash_key, "empty", 0, winreg.REG_SZ, empty_trash_path)
                if full_trash_path and os.path.exists(full_trash_path):
                    winreg.SetValueEx(trash_key, "full", 0, winreg.REG_SZ, full_trash_path)
            winreg.CloseKey(trash_key)
        except Exception: pass

    def play_sound_direct(self, path):
        if path and os.path.exists(path):
            winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)

    def restart_shell(self):
        """Контролируемое закрытие Проводника через PowerShell. Вычищает буферы дескрипторов под ноль!"""
        try:
            time.sleep(0.3)
            # Командуем Windows корректно закрыть Проводник и освободить буферы USER/GDI хендлов
            subprocess.run('powershell -Command "Stop-Process -Name explorer -Force"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(0.4) # Время на полное очищение графического контекста ОЗУ
            
            # Поднимаем чистую оболочку
            os.system(config.CMD_START_EXPLORER)
            time.sleep(0.5)
            # Обновляем рабочий стол
            ctypes.windll.shell32.SHChangeNotify(0x08000000, 0x1000, None, None)
            print("[Ядро] Графические буферы успешно очищены, Проводник поднят.")
        except Exception:
            # Аварийный откат, если PowerShell заблокирован политиками ОС
            os.system(config.CMD_KILL_EXPLORER)
            time.sleep(0.2)
            os.system(config.CMD_START_EXPLORER)
