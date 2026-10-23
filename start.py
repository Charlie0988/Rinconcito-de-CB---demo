# start.py
import threading
import time
import subprocess
from scripts.sync_booking import sync_all_calendars

def sync_loop():
    while True:
        try:
            sync_all_calendars()
        except Exception as e:
            print("Error en la sincronización de calendarios:", e)
        time.sleep(1800)  # cada 30 minutos

# Lanzamos la sincronización en segundo plano
threading.Thread(target=sync_loop, daemon=True).start()

# Arrancamos el servidor de Silence normalmente, en primer plano
subprocess.run(["silence", "run"])