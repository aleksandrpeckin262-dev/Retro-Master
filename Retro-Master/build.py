import subprocess
import sys
import os

# Имя твоего главного файла
MAIN_SCRIPT = "main.py"

# Название иконки (если она есть в конфиге)
# Если иконки нет, PyInstaller просто соберет со стандартной
ICON_FILE = "icon.ico" 

print("[*] Начало сборки проекта Retro-Master v1.2+ ...")

# Базовые флаги для PyInstaller:
# --onefile : собирает всё в один .exe
# --noconsole : скрывает черное окно консоли при запуске GUI
# --clean : очищает кэш перед сборкой
build_command = [
    sys.executable, "-m", "PyInstaller",
    "--onefile",
    "--noconsole",
    "--clean",
    "--name=Retro-Master_v1.2"
]

# Если в папке проекта лежит файл иконки, добавляем его в сборку
if os.path.exists(ICON_FILE):
    build_command.append(f"--icon={ICON_FILE}")
else:
    print("[!] Файл icon.ico не найден в текущей папке, сборка пройдет со стандартной иконкой.")

# Добавляем главный скрипт в конец команды
build_command.append(MAIN_SCRIPT)

try:
    # Запуск сборки
    subprocess.run(build_command, check=True)
    print("\n[+] СБОРКА ЗАВЕРШЕНА УСПЕШНО!")
    print("[+] Твой готовый файл лежит в папке: dist/Retro-Master_v1.2.exe")
    print("[*] Папки 'build' и 'dist' созданы автоматически в директории проекта.")
except subprocess.CalledProcessError as e:
    print(f"\n[-] Ошибка при сборке проекта: {e}")
except FileNotFoundError:
    print("\n[-] Ошибка: PyInstaller не установлен в системе.")
    print("[*] Установи его командой: pip install pyinstaller")
