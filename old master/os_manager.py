import ctypes, os, winreg, winsound, time, config

class WindowsManager:
    def set_wallpaper_from_buffer(self, file_bytes, temp_name="temp_wp.jpg"):
        """Безопасно натягивает обои из бинарного буфера памяти ОЗУ"""
        if not file_bytes: return
        try:
            temp_path = os.path.abspath(os.path.join(config.BASE_DIR, temp_name))
            with open(temp_path, "wb") as f:
                f.write(file_bytes)
            if os.path.exists(temp_path):
                ctypes.windll.user32.SystemParametersInfoW(config.SPI_SETDESKWALLPAPER, 0, temp_path, config.SPI_FLAGS_IMMEDIATE)
        except Exception as e:
            print(f"[Ядро] Ошибка буфера обоев: {e}")

    def set_all_cursors_from_buffer(self, cursor_buffers, is_reset=False):
        """Пакетно шьет курсоры из готовых буферов ОЗУ, защищая мышь от фризов"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Cursors", 0, winreg.KEY_SET_VALUE)
            for name in config.CURSOR_NAMES:
                if is_reset:
                    sys_cur = os.path.join(r"C:\Windows\Cursors", f"aero_{name.lower()}.cur")
                    if not os.path.exists(sys_cur): sys_cur = os.path.join(r"C:\Windows\Cursors", f"{name.lower()}.cur")
                    winreg.SetValueEx(key, name, 0, winreg.REG_SZ, sys_cur if os.path.exists(sys_cur) else "")
                else:
                    c_bytes, ext = cursor_buffers.get(name.lower(), (None, ".cur"))
                    if c_bytes:
                        temp_cur_path = os.path.abspath(os.path.join(config.BASE_DIR, f"temp_{name.lower()}{ext}"))
                        with open(temp_cur_path, "wb") as f: f.write(c_bytes)
                        winreg.SetValueEx(key, name, 0, winreg.REG_SZ, temp_cur_path)
            winreg.CloseKey(key)
            ctypes.windll.user32.SystemParametersInfoW(config.SPI_SETCURSORS, 0, 0, config.SPI_FLAGS_IMMEDIATE)
        except Exception as e:
            print(f"[Ядро] Ошибка буфера курсоров: {e}")

    def play_sound_from_buffer(self, sound_bytes):
        """Проигрывает звук старта мгновенно прямо из оперативной памяти ОЗУ"""
        if sound_bytes:
            try:
                winsound.PlaySound(sound_bytes, winsound.SND_MEMORY | winsound.SND_ASYNC)
            except Exception: pass

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
                try:
                    winreg.DeleteValue(dwm_key, "AccentColor")
                    winreg.DeleteValue(dwm_key, "AccentColorInactive")
                except FileNotFoundError: pass
            winreg.CloseKey(dwm_key)
        except Exception: pass

    def set_system_icons_from_buffer(self, comp_bytes, empty_trash_bytes, full_trash_bytes, is_reset=False):
        """Шьет системные иконки из буферов памяти ОЗУ"""
        try:
            comp_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, config.REG_PATH_COMP_ICON)
            if is_reset:
                try: winreg.DeleteValue(comp_key, "")
                except FileNotFoundError: pass
            elif comp_bytes:
                temp_path = os.path.abspath(os.path.join(config.BASE_DIR, "temp_computer.ico"))
                with open(temp_path, "wb") as f: f.write(comp_bytes)
                winreg.SetValueEx(comp_key, "", 0, winreg.REG_SZ, temp_path)
            winreg.CloseKey(comp_key)

            trash_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, config.REG_PATH_TRASH_ICON)
            if is_reset:
                try: winreg.DeleteValue(trash_key, ""); winreg.DeleteValue(trash_key, "empty"); winreg.DeleteValue(trash_key, "full")
                except FileNotFoundError: pass
            else:
                if empty_trash_bytes:
                    t_empty = os.path.abspath(os.path.join(config.BASE_DIR, "temp_t_empty.ico"))
                    with open(t_empty, "wb") as f: f.write(empty_trash_bytes)
                    winreg.SetValueEx(trash_key, "", 0, winreg.REG_SZ, t_empty)
                    winreg.SetValueEx(trash_key, "empty", 0, winreg.REG_SZ, t_empty)
                if full_trash_bytes:
                    t_full = os.path.abspath(os.path.join(config.BASE_DIR, "temp_t_full.ico"))
                    with open(t_full, "wb") as f: f.write(full_trash_bytes)
                    winreg.SetValueEx(trash_key, "full", 0, winreg.REG_SZ, t_full)
            winreg.CloseKey(trash_key)
        except Exception: pass

    def restart_shell(self):
        try:
            time.sleep(0.3)
            os.system(config.CMD_KILL_EXPLORER)
            time.sleep(0.2)
            os.system(config.CMD_START_EXPLORER)
            time.sleep(0.5)
            ctypes.windll.shell32.SHChangeNotify(0x08000000, 0x1000, None, None)
        except Exception: pass
