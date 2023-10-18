import json
from datetime import datetime, timedelta


def reminder_session():
    with open("JSON/temporary.json", "r", encoding="utf-8") as to_read:
        check_information = json.load(to_read)

        today = datetime.now()
        
        # Calcular la fecha 10 días después
        to_10_days = today + timedelta(days=10)

        # Agregar nuevos elementos al diccionario
        check_information["active"] = True
        check_information["time_to_disconnect"] = to_10_days.strftime("%Y-%m-%d %H:%M:%S")

    with open("JSON/temporary.json", "w", encoding="utf-8") as to_write:
        json.dump(check_information, to_write, indent=4)