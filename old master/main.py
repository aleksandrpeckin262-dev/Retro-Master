import os, tkinter as tk, threading, config, time
from os_manager import WindowsManager

class GUE(tk.Tk):
    def __init__(self):
        super().__init__()
        self.os_manager = WindowsManager()
        self.title(config.WINDOW_TITLE); self.geometry(config.WINDOW_GEOMETRY); self.resizable(False, False)
        if os.path.exists(config.ICON_PATH): self.iconbitmap(config.ICON_PATH)
        
        print("[Буферизация] Загрузка ресурсов в оперативную память...")
        self.ram_cache = {}
        self.load_all_resources_to_ram()
        
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

    def load_all_resources_to_ram(self):
        for os_name, paths in config.THEME_RESOURCES.items():
            self.ram_cache[os_name] = {}
            for key in ["wallpaper", "sound_start", "sound_close", "icon_computer", "icon_trash_empty", "icon_trash_full"]:
                p = paths.get(key)
                if p and os.path.exists(p) and os.path.isfile(p):
                    with open(p, "rb") as f: self.ram_cache[os_name][key] = f.read()
            
            cur_dir = paths.get("cursors_dir") or paths.get("cursors_old_dir")
            if cur_dir and os.path.exists(cur_dir):
                self.ram_cache[os_name]["cursors"] = {}
                for c_name in config.CURSOR_NAMES:
                    for f in os.listdir(cur_dir):
                        if f.lower().startswith(c_name.lower()):
                            p_cur = os.path.join(cur_dir, f)
                            ext = os.path.splitext(f)[1]
                            with open(p_cur, "rb") as f_c:
                                self.ram_cache[os_name]["cursors"][c_name.lower()] = (f_c.read(), ext)
        print("[Буферизация] Все файлы успешно висят в оперативной памяти!")

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
            
            buf = self.ram_cache.get(v, {})
            self.os_manager.play_sound_from_buffer(buf.get("sound_start"))
            self.os_manager.set_wallpaper_from_buffer(buf.get("wallpaper"), f"temp_wp_{v}.jpg")
            self.os_manager.set_all_cursors_from_buffer(buf.get("cursors", {}), is_reset=False)
            self.os_manager.set_system_icons_from_buffer(buf.get("icon_computer"), buf.get("icon_trash_empty"), buf.get("icon_trash_full"), is_reset=False)
            
            self.os_manager.set_clear_type(enable=(v != "win95" and v != "win98"))
            self.os_manager.set_retro_taskbar_color(enable=(v in ["win95", "win98"]))
            self.os_manager.set_retro_colors_win32(version_name=v, enable=(v in ["win95", "win98"]))
            
            if ft: ft.join()
            time.sleep(0.5); self.os_manager.restart_shell()
            print(f"[Успех] Тема {v} развернута мгновенно из буфера памяти!")
        threading.Thread(target=run_backend, daemon=True).start()

    def restore_theme(self):
        self.update_idletasks()
        def run_restore():
            ft = threading.Thread(target=self.os_manager.set_global_font_substitute, args=(None,), daemon=True); ft.start()
            buf = self.ram_cache.get("restore", {})
            
            self.os_manager.play_sound_from_buffer(buf.get("sound_close"))
            self.os_manager.set_wallpaper_from_buffer(buf.get("wallpaper"), "temp_wp_restore.jpg")
            self.os_manager.set_all_cursors_from_buffer({}, is_reset=True)
            self.os_manager.set_system_icons_from_buffer(None, None, None, is_reset=True)
            
            self.os_manager.set_clear_type(enable=True)
            self.os_manager.set_retro_taskbar_color(enable=False); self.os_manager.set_retro_colors_win32(version_name="default", enable=False)
            
            if ft: ft.join()
            time.sleep(0.5); self.os_manager.restart_shell()
            print("[Успех] Система чисто возвращена к Windows 10!")
        threading.Thread(target=run_restore, daemon=True).start()

if __name__ == "__main__":
    app = GUE()
    app.mainloop()
