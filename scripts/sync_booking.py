import os
import re
import socket
import requests
import mysql.connector

# Añade aquí la URL de iCal de cada plataforma
ICAL_SOURCES = {
    'booking': os.environ.get('ICAL_BOOKING'), 
    'airbnb': os.environ.get('ICAL_AIRBNB'), 
    'vrbo': os.environ.get('ICAL_VRBO'), 
    'hometogo': os.environ.get('ICAL_HOMETOGO'), 
    'thehomecake': os.environ.get('ICAL_THEHOMECAKE'), 
} 

ICAL_SOURCES = {
    k: v for k, v in ICAL_SOURCES.items() if v
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Accept": "text/calendar,text/plain,*/*",
    "Accept-Language": "es-ES,es;q=0.9",
}

def fetch_ranges(url):
    resp = requests.get(url, timeout=15, headers=HEADERS)
    resp.raise_for_status()
    text = resp.text
    events = re.findall(r"BEGIN:VEVENT[\s\S]*?END:VEVENT", text)
    ranges = []
    for ev in events:
        start = re.search(r"DTSTART.*?:(\d{8})", ev)
        end = re.search(r"DTEND.*?:(\d{8})", ev)
        if start and end:
            ranges.append((start.group(1), end.group(1)))
    return ranges

def sync_all_calendars():
    db_host = os.environ["AIVEN_HOST"]
    db_port = int(os.environ["AIVEN_PORT"])
    resolved_ip = socket.gethostbyname(db_host)

    conn = mysql.connector.connect(
        host=resolved_ip, port=db_port,
        user=os.environ["AIVEN_USER"], password=os.environ["AIVEN_PASSWORD"],
        database=os.environ["AIVEN_DATABASE"],
        ssl_ca="ca.pem", ssl_verify_cert=False, ssl_disabled=False,
    )
    cur = conn.cursor()

    for name, url in ICAL_SOURCES.items():
        try:
            ranges = fetch_ranges(url)
            cur.execute("DELETE FROM booked_dates WHERE source = %s", (name,))
            cur.executemany(
                "INSERT INTO booked_dates (start_date, end_date, source) VALUES (%s, %s, %s)",
                [(s, e, name) for s, e in ranges]
            )
            conn.commit()
            print(f"{name}: {len(ranges)} reservas actualizadas")
        except Exception as e:
            # Si falla, NO tocamos las filas de esta plataforma que ya hab\u00eda en la tabla
            print(f"Aviso: no se pudo leer {name}, se mantienen sus datos anteriores: {e}")

    cur.close()
    conn.close()

if __name__ == "__main__":
    sync_all_calendars()