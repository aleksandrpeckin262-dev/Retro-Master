import os
import tkinter as tk
import threading
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
            
        required_folders = [
            config.FOLDER_BG_NOW, config.FOLDER_BG_OLD, 
            config.FOLDER_CUR_NOW, config.FOLDER_CUR_OLD, 
            config.FOLDER_SOUNDS_NOW, config.FOLDER_ICO_NOW, 
            config.FOLDER_ICO_OLD
        ]
        for folder_path in required_folders:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            
        self.selected_version = tk.StringVar(value="win95")
        
        self.label_title = tk.Label(self, text="Select OS Theme:")
        self.label_title.place(x=20, y=20)
        
        self.radio_win95 = tk.Radiobutton(self, text="Windows 95", variable=self.selected_version, value="win95", command=self.update_app_style)
        self.radio_win95.place(x=20, y=50)
        
        self.radio_win98 = tk.Radiobutton(self, text="Windows 98", variable=self.selected_version, value="win98", command=self.update_app_style)
        self.radio_win98.place(x=20, y=80)
        
        self.radio_winXP = tk.Radiobutton(self, text="Windows XP", variable=self.selected_version, value="winXP", command=self.update_app_style)
        self.radio_winXP.place(x=20, y=110)
        
        self.radio_vista = tk.Radiobutton(self, text="Windows Vista", variable=self.selected_version, value="vista", command=self.update_app_style)
        self.radio_vista.place(x=20, y=140)
        
        self.radio_win7 = tk.Radiobutton(self, text="Windows 7", variable=self.selected_version, value="win7", command=self.update_app_style)
        self.radio_win7.place(x=20, y=170)
        
        self.all_radios = [self.radio_win95, self.radio_win98, self.radio_winXP, self.radio_vista, self.radio_win7]
        
        self.button_start = tk.Button(self, text="Start", command=self.apply_theme)
        self.button_start.place(x=220, y=40, width=140, height=45)
        
        self.button_reset = tk.Button(self, text="Reset", command=self.restore_theme)
        self.button_reset.place(x=220, y=110, width=140, height=45)
        
        self.button_exit = tk.Button(self, text="Exit", command=self.destroy)
        self.button_exit.place(x=220, y=180, width=140, height=45)
        
        self.update_app_style()

    def update_app_style(self):
        version = self.selected_version.get()
        
        if version == "win95":
            app_bg = config.COLOR_BG_TEAL
            btn_bg = "#D4D0C8"            
            btn_active = "#B0B0B0"
            btn_fg = "#000000"            
            app_font = ("MS Sans Serif", 11)
            text_color = "#FFFFFF"
            btn_relief = "raised"         
            btn_bd = 3
            
        elif version == "win98":
            app_bg = "#007070"
            btn_bg = "#D4D0C8"            
            btn_active = "#B0B0B0"
            btn_fg = "#000000"            
            app_font = ("MS Sans Serif", 11)
            text_color = "#FFFFFF"
            btn_relief = "raised"         
            btn_bd = 2 
            
        elif version == "winXP":
            app_bg = "#245DD7"            
            btn_bg = "#5B9BD5"            
            btn_active = "#41719C"
            btn_fg = "#FFFFFF"            
            app_font = ("Tahoma", 11)     
            text_color = "#FFFFFF"
            btn_relief = "flat"           
            btn_bd = 1
            
        elif version == "vista":
            app_bg = "#202020"            
            btn_bg = "#0078D7"          
            btn_active = "#005A9E"
            btn_fg = "#FFFFFF"
            app_font = ("Segoe UI", 11) 
            text_color = "#FFFFFF"
            btn_relief = "flat"           
            btn_bd = 0
            
        elif version == "win7":
            app_bg = "#0354AD"
            btn_bg = "#11B7EB"            
            btn_active = "#0E96C2"
            btn_fg = "#000000"            
            app_font = ("Segoe UI", 11)
            text_color = "#FFFFFF"
            btn_relief = "raised"         
            btn_bd = 1
            
        self.configure(bg=app_bg)
        self.label_title.configure(bg=app_bg, fg=text_color, font=app_font)
        
        for radio in self.all_radios:
            radio.configure(bg=app_bg, fg=text_color, activebackground=app_bg, activeforeground=text_color, font=app_font)
        
        for btn in [self.button_start, self.button_reset, self.button_exit]:
            btn.configure(bg=btn_bg, fg=btn_fg, activebackground=btn_active, activeforeground=btn_fg, font=app_font, relief=btn_relief, bd=btn_bd)

    def apply_theme(self):
        version = self.selected_version.get()
        
        def run_backend():
            if version == "win95":
                self.os_manager.play_sound(config.SOUND_START)
                bg_file = self.os_manager.get_first_file(config.FOLDER_BG_NOW)
                self.os_manager.set_wallpaper(bg_file)
                self.os_manager.set_all_cursors(config.FOLDER_CUR_NOW, is_reset=False)
                self.os_manager.set_clear_type(enable=False)
                self.os_manager.set_global_font_substitute("MS Sans Serif")
                self.os_manager.set_retro_colors_win32(version_name="win95", enable=True)
                self.os_manager.set_system_icons(is_reset=False)
                self.os_manager.set_retro_taskbar_color(enable=True)
                self.os_manager.restart_shell()
                print("Стиль Windows 95 успешно активирован!")
                
            elif version == "win98":
                self.os_manager.play_sound(config.SOUND_START)
                bg_file = self.os_manager.get_first_file(config.FOLDER_BG_NOW)
                self.os_manager.set_wallpaper(bg_file)
                self.os_manager.set_all_cursors(config.FOLDER_CUR_NOW, is_reset=False)
                self.os_manager.set_clear_type(enable=False)
                self.os_manager.set_global_font_substitute("MS Sans Serif")
                self.os_manager.set_system_icons(is_reset=False)
                self.os_manager.set_retro_taskbar_color(enable=True)
                self.os_manager.set_retro_colors_win32(version_name="win98", enable=True)
                self.os_manager.restart_shell()
                print("Стиль Windows 98 успешно активирован!")
                
            elif version in ["winXP", "vista", "win7"]:
                print(f"[В разработке] Скрипты для {version} будут добавлены в следующем обновлении!")

        threading.Thread(target=run_backend, daemon=True).start()

    def restore_theme(self):
        version = self.selected_version.get()
        
        def run_restore():
            if version in ["win95", "win98"]:
                self.os_manager.play_sound(config.SOUND_CLOSE)
                bg_file = self.os_manager.get_first_file(config.FOLDER_BG_OLD)
                self.os_manager.set_wallpaper(bg_file)
                self.os_manager.set_all_cursors(config.FOLDER_CUR_OLD, is_reset=True)
                self.os_manager.set_clear_type(enable=True)
                self.os_manager.set_global_font_substitute(None)
                self.os_manager.set_retro_colors_win32(version_name="default", enable=False)
                self.os_manager.set_system_icons(is_reset=True)
                self.os_manager.set_retro_taskbar_color(enable=False)
                self.os_manager.restart_shell()
                print("Настройки Windows 10 восстановлены!")
            else:
                print(f"[В разработке] Сброс для {version} будет добавлен позже.")

        threading.Thread(target=run_restore, daemon=True).start()

if __name__ == "__main__":
    app = GUE()
    app.mainloop()
