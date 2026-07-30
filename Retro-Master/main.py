import os
import tkinter as tk
import threading
import time
import ctypes
import config
from os_manager import WindowsManager

class GUE(tk.Tk):
    def __init__(self):
        super().__init__()
        self.os_manager = WindowsManager()
        self.title(config.WINDOW_TITLE)
        self.geometry(config.WINDOW_GEOMETRY)
        self.resizable(False, False)
        
        if os.path.exists(config.ICON_PATH): 
            self.iconbitmap(config.ICON_PATH)
        
        # Переменная для Tkinter радио-кнопок
        self.selected_version = tk.StringVar(value="win95")
        
        # ХРАНИЛИЩЕ ТЕКУЩЕЙ ТЕМЫ: Запоминаем, какая тема РЕАЛЬНО активна в системе сейчас.
        # По умолчанию при старте считаем, что это стандартная Windows 10 (None).
        self.current_theme = None 
        
        self.label_title = tk.Label(self, text="Select OS Theme:")
        self.label_title.place(x=20, y=20)
        
        versions_list = [
            ("Windows 95", "win95", 50), 
            ("Windows 98", "win98", 80), 
            ("Windows XP", "winXP", 110), 
            ("Windows Vista", "vista", 140), 
            ("Windows 7", "win7", 170)
        ]
        
        for text, version_code, y_position in versions_list:
            radio_btn = tk.Radiobutton(
                self, text=text, variable=self.selected_version, 
                value=version_code, command=self.update_app_style
            )
            radio_btn.place(x=20, y=y_position)
            
        self.all_radios = [widget for widget in self.winfo_children() if isinstance(widget, tk.Radiobutton)]
        
        tk.Button(self, text="Start", command=self.apply_theme).place(x=220, y=40, width=140, height=45)
        tk.Button(self, text="Reset", command=self.restore_theme).place(x=220, y=110, width=140, height=45)
        tk.Button(self, text="Exit", command=self.destroy).place(x=220, y=180, width=140, height=45)
        
        self.all_btns = [widget for widget in self.winfo_children() if isinstance(widget, tk.Button)]
        self.update_app_style()

    def update_app_style(self):
        current_version = self.selected_version.get()
        
        for button in self.all_btns: 
            button.configure(image="", compound="none")
            
        if current_version == "win95": 
            app_bg, btn_bg, btn_act, btn_fg, font, text_c, relief, bd = config.COLOR_BG_TEAL, "#D4D0C8", "#B0B0B0", "#000000", ("MS Sans Serif", 11), "#FFFFFF", "raised", 3
        elif current_version == "win98": 
            app_bg, btn_bg, btn_act, btn_fg, font, text_c, relief, bd = "#007070", "#D4D0C8", "#B0B0B0", "#000000", ("MS Sans Serif", 11), "#FFFFFF", "raised", 2
        elif current_version == "winXP": 
            app_bg, btn_bg, btn_act, btn_fg, font, text_c, relief, bd = "#245DD7", "#5B9BD5", "#41719C", "#FFFFFF", ("Tahoma", 11), "#FFFFFF", "flat", 1
        elif current_version == "vista": 
            app_bg, btn_bg, btn_act, btn_fg, font, text_c, relief, bd = "#202020", "#0078D7", "#005A9E", "#FFFFFF", ("Segoe UI", 11), "#FFFFFF", "flat", 0
        elif current_version == "win7": 
            app_bg, btn_bg, btn_act, btn_fg, font, text_c, relief, bd = "#0354AD", "#11B7EB", "#0E96C2", "#000000", ("Segoe UI", 11), "#FFFFFF", "raised", 1
            
        self.configure(bg=app_bg)
        self.label_title.configure(bg=app_bg, fg=text_c, font=font)
        
        for radio in self.all_radios: 
            active_bg = "#19398a" if current_version == "winXP" else app_bg
            radio.configure(bd=0, highlightthickness=0, bg=app_bg, fg=text_c, activebackground=active_bg, activeforeground=text_c, font=font)
            
        for button in self.all_btns: 
            button.configure(bg=btn_bg, fg=btn_fg, activebackground=btn_act, activeforeground=btn_fg, font=font, relief=relief, bd=bd)

    def apply_theme(self):
        target_version = self.selected_version.get()
        self.update_idletasks()
        
        def run_backend():
            target_font = "MS Sans Serif" if target_version in ["win95", "win98"] else ("Tahoma" if target_version == "winXP" else "Segoe UI")
            self.os_manager.set_global_font_substitute(target_font)
            
            resource_pack = config.THEME_RESOURCES.get(target_version)
            
            self.os_manager.set_retro_taskbar_color(enable=False)
            self.os_manager.set_retro_colors_win32(version_name="default", enable=False)
            
            self.os_manager.play_sound_direct(resource_pack.get("sound_start"))
            self.os_manager.set_wallpaper(resource_pack.get("wallpaper"))
            self.os_manager.set_all_cursors_direct(resource_pack.get("cursors_dir"), is_reset=False)
            self.os_manager.set_system_icons_direct(resource_pack.get("icon_computer"), resource_pack.get("icon_trash_empty"), resource_pack.get("icon_trash_full"), is_reset=False)
            
            self.os_manager.set_clear_type(enable=(target_version != "win95" and target_version != "win98"))
            
            if target_version in ["win95", "win98"]:
                self.os_manager.set_retro_taskbar_color(enable=True)
                self.os_manager.set_retro_colors_win32(version_name=target_version, enable=True)
                if target_version == "win98": 
                    self.os_manager.set_explorer_click_sound_direct(resource_pack.get("sound_click"), enable=True)
            
            ctypes.windll.user32.SendMessageW(config.HWND_BROADCAST, config.WM_SETTINGCHANGE, 0, "Registry::String")
            time.sleep(0.8)
            
            self.os_manager.restart_shell()
            
            # УСПЕХ: Тема применилась, записываем её имя в память программы
            self.current_theme = target_version
            
        threading.Thread(target=run_backend, daemon=True).start()

    def restore_theme(self):
        self.update_idletasks()
        
        def run_restore():
            # 1. ДИНАМИЧЕСКИЙ ВЫЗОВ ЗВУКА: Ищем кастомный звук закрытия уходящей темы
            sound_to_play = None
            if self.current_theme:
                # Заглядываем в конфиг той темы, которая включена ПРЯМО СЕЙЧАС
                old_pack = config.THEME_RESOURCES.get(self.current_theme)
                if old_pack:
                    sound_to_play = old_pack.get("sound_close")
            
            # Воспроизводим найденный кастомный звук закрытия (если темы не было, будет тишина)
            if sound_to_play:
                self.os_manager.play_sound_direct(sound_to_play)
                
            self.os_manager.set_global_font_substitute(None)
            resource_pack = config.THEME_RESOURCES["restore"]
            
            # Удалена строчка жесткого проигрывания звука из секции "restore"
            self.os_manager.set_wallpaper(resource_pack.get("wallpaper"))
            self.os_manager.set_all_cursors_direct(resource_pack.get("cursors_old_dir"), is_reset=True)
            self.os_manager.set_clear_type(enable=True)
            self.os_manager.set_explorer_click_sound_direct(None, enable=False)
            self.os_manager.set_system_icons_direct(None, None, None, is_reset=True)
            self.os_manager.set_retro_taskbar_color(enable=False)
            self.os_manager.set_retro_colors_win32(version_name="default", enable=False)
            
            ctypes.windll.user32.SendMessageW(config.HWND_BROADCAST, config.WM_SETTINGCHANGE, 0, "Registry::String")
            time.sleep(0.8)
            
            self.os_manager.restart_shell()
            
            # Сбрасываем текущую тему обратно на дефолтную Windows 10
            self.current_theme = None
            
        threading.Thread(target=run_restore, daemon=True).start()

if __name__ == "__main__":
    app = GUE()
    app.mainloop()
