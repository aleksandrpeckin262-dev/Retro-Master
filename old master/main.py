import os, tkinter as tk, threading, config, time
from os_manager import WindowsManager

class GUE(tk.Tk):
    def __init__(self):
        super().__init__()
        self.os_manager = WindowsManager()
        self.title(config.WINDOW_TITLE); self.geometry(config.WINDOW_GEOMETRY); self.resizable(False, False)
        if os.path.exists(config.ICON_PATH): self.iconbitmap(config.ICON_PATH)
        
        self.bg_image_xp = tk.PhotoImage(file=config.PATH_IMAGE_XP) if os.path.exists(config.PATH_IMAGE_XP) else None
        self.selected_version = tk.StringVar(value="win95")
        self.bg_canvas = tk.Canvas(self, width=400, height=300, bd=0, highlightthickness=0)
        if self.bg_image_xp: self.bg_canvas.create_image(0, 0, image=self.bg_image_xp, anchor="nw")
        
        self.label_title = tk.Label(self, text="Select OS Theme:"); self.label_title.place(x=20, y=20)
        versions = [("Windows 95", "win95", 50), ("Windows 98", "win98", 80), ("Windows XP", "winXP", 110), ("Windows Vista", "vista", 140), ("Windows 7", "win7", 170)]
        for t, v, y in versions:
            rb = tk.Radiobutton(self, text=t, variable=self.selected_version, value=v, command=self.update_app_style); rb.place(x=20, y=y)
        self.all_radios = [w for w in self.winfo_children() if isinstance(w, tk.Radiobutton)]
        
        tk.Button(self, text="Start", command=self.apply_theme).place(x=220, y=40, width=140, height=45)
        tk.Button(self, text="Reset", command=self.restore_theme).place(x=220, y=110, width=140, height=45)
        tk.Button(self, text="Exit", command=self.destroy).place(x=220, y=180, width=140, height=45)
        self.all_btns = [w for w in self.winfo_children() if isinstance(w, tk.Button)]; self.update_app_style()

    def update_app_style(self):
        v = self.selected_version.get()
        for b in self.all_btns: b.configure(image="", compound="none")
        if v == "win95": app_bg, btn_bg, btn_act, btn_fg, font, text_c, relief, bd = config.COLOR_BG_TEAL, "#D4D0C8", "#B0B0B0", "#000000", ("MS Sans Serif", 11), "#FFFFFF", "raised", 3
        elif v == "win98": app_bg, btn_bg, btn_act, btn_fg, font, text_c, relief, bd = "#007070", "#D4D0C8", "#B0B0B0", "#000000", ("MS Sans Serif", 11), "#FFFFFF", "raised", 2
        elif v == "winXP": app_bg, btn_bg, btn_act, btn_fg, font, text_c, relief, bd = "#245DD7", "#5B9BD5", "#41719C", "#FFFFFF", ("Tahoma", 11), "#FFFFFF", "flat", 1
        elif v == "vista": app_bg, btn_bg, btn_act, btn_fg, font, text_c, relief, bd = "#202020", "#0078D7", "#005A9E", "#FFFFFF", ("Segoe UI", 11), "#FFFFFF", "flat", 0
        elif v == "win7": app_bg, btn_bg, btn_act, btn_fg, font, text_c, relief, bd = "#0354AD", "#11B7EB", "#0E96C2", "#000000", ("Segoe UI", 11), "#FFFFFF", "raised", 1
            
        if v == "winXP" and self.bg_image_xp:
            self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1); self.bg_canvas.configure(bg=app_bg); self.label_title.lift()
            for r in self.all_radios: r.lift()
            for b in self.all_btns: b.lift()
            self.label_title.configure(bg=app_bg, fg=text_c, font=font)
            for r in self.all_radios: r.configure(bd=0, highlightthickness=0, bg=app_bg, fg=text_c, activebackground="#19398a", activeforeground=text_c, font=font)
        else:
            self.bg_canvas.place_forget(); self.configure(bg=app_bg); self.label_title.configure(bg=app_bg, fg=text_c, font=font)
            for r in self.all_radios: r.configure(bd=0, highlightthickness=0, bg=app_bg, fg=text_c, activebackground=app_bg, activeforeground=text_c, font=font)
        for b in self.all_btns: b.configure(bg=btn_bg, fg=btn_fg, activebackground=btn_act, activeforeground=btn_fg, font=font, relief=relief, bd=bd)

    def apply_theme(self):
        v = self.selected_version.get(); self.update_idletasks()
        def run_backend():
            tf = "MS Sans Serif" if v in ["win95", "win98"] else ("Tahoma" if v == "winXP" else "Segoe UI")
            ft = threading.Thread(target=self.os_manager.set_global_font_substitute, args=(tf,), daemon=True); ft.start()
            res = config.THEME_RESOURCES.get(v)
            
            # Принудительная зачистка ОЗУ от старых ретро-эффектов до переключения
            self.os_manager.set_retro_taskbar_color(enable=False)
            self.os_manager.set_retro_colors_win32(version_name="default", enable=False)
            
            self.os_manager.play_sound_direct(res.get("sound_start"))
            self.os_manager.set_wallpaper(res.get("wallpaper"))
            self.os_manager.set_all_cursors_direct(res.get("cursors_dir"), is_reset=False)
            self.os_manager.set_system_icons_direct(res.get("icon_computer"), res.get("icon_trash_empty"), res.get("icon_trash_full"), is_reset=False)
            self.os_manager.set_clear_type(enable=(v != "win95" and v != "win98"))
            
            if v in ["win95", "win98"]:
                self.os_manager.set_retro_taskbar_color(enable=True)
                self.os_manager.set_retro_colors_win32(version_name=v, enable=True)
                if v == "win98": self.os_manager.set_explorer_click_sound_direct(res.get("sound_click"), enable=True)
            
            if ft: ft.join()
            
            # Аппаратный сброс буферов Windows на живую оболочку
            import ctypes
            ctypes.windll.user32.SendMessageW(config.HWND_BROADCAST, config.WM_SETTINGCHANGE, 0, "Registry::String")
            time.sleep(0.8)
            
            self.os_manager.restart_shell()
            print(f"[Успех] Тема {v} полностью развернута!")
        threading.Thread(target=run_backend, daemon=True).start()

    def restore_theme(self):
        self.update_idletasks()
        def run_restore():
            ft = threading.Thread(target=self.os_manager.set_global_font_substitute, args=(None,), daemon=True); ft.start()
            res = config.THEME_RESOURCES["restore"]
            
            self.os_manager.play_sound_direct(res.get("sound_close"))
            self.os_manager.set_wallpaper(res.get("wallpaper"))
            self.os_manager.set_all_cursors_direct(res.get("cursors_old_dir"), is_reset=True)
            self.os_manager.set_clear_type(enable=True); self.os_manager.set_explorer_click_sound_direct(None, enable=False)
            self.os_manager.set_system_icons_direct(None, None, None, is_reset=True)
            self.os_manager.set_retro_taskbar_color(enable=False); self.os_manager.set_retro_colors_win32(version_name="default", enable=False)
            
            if ft: ft.join()
            
            import ctypes
            ctypes.windll.user32.SendMessageW(config.HWND_BROADCAST, config.WM_SETTINGCHANGE, 0, "Registry::String")
            time.sleep(0.8)
            
            self.os_manager.restart_shell()
            print("[Успех] Система чисто возвращена к Windows 10!")
        threading.Thread(target=run_restore, daemon=True).start()

if __name__ == "__main__":
    app = GUE()
    app.mainloop()

