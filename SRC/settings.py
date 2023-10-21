import json
import os
from screeninfo import get_monitors
import hashlib
import time

with open('JSON/settings.json', 'r') as f:
    settings = json.load(f)

    version = settings['app_settings']['version']
    name = settings['app_settings']['name']
    language = settings['app_settings']['language']
    license = settings['app_settings']['license']

APP_REQUERIMENTS = (
    version,
    name,
    language,
    license
)

USER_SESSION = {}

PYTHON_VERSION = "3.11.5 ABAS"

with open("JSON/information.json", 'r', encoding="utf-8") as file:
    informations = json.load(file)

APP_INFORMATIONS = {
    "info1": informations["info1"],
    "info2": informations["info2"]
}


def proccess_log(**kwargs):
    with open("JSON/temporary.json", "w", encoding="utf-8") as proccess:
        json.dump({
            "user_information": kwargs, "data": {
                "number_of_products": 0,
            }
        }, proccess, indent=4)
    with open("JSON/temporary.json", "r", encoding="utf-8") as proccess:
        loader = json.load(proccess)


def check_log():
    try:
        if os.path.exists("JSON/temporary.json"):
            with open("JSON/temporary.json", "r", encoding="utf-8") as check:
                checked = json.load(check)
                if "user_information" in checked:
                    if "logued" not in checked["user_information"]:
                        return False
                    else:
                        USER_SESSION["COMPANY_NAME"] = checked["user_information"]["enterprise_name"]
                        USER_SESSION["COMPANY_ID"] = checked["user_information"]["id"]
                        return True
                else:
                    return False
        else:
            return False
    except json.decoder.JSONDecodeError as e:
        print(f"Error al cargar el archivo JSON: {e}")
        return False


monitor = get_monitors()

for monitores in monitor:
    width = monitores.width
    height = monitores.height

pw = width * 0.90
ph = height * 0.92

LAST_WINDOW = {}


def hash_pass(**passwd):
    psw = hashlib.sha256(passwd["pass_auth_user_get_input"].encode()).hexdigest()
    return psw


def formatt(*args):
    return "{:,.2f}".format(args[0])

def check_session() -> bool:
    with open("JSON/temporary.json", "r", encoding="utf-8") as check:
        checked = json.load(check)
        if "active" in checked:
            USER_SESSION["COMPANY_NAME"] = checked["user_information"]["enterprise_name"]
            USER_SESSION["COMPANY_ID"] = checked["user_information"]["id"]
            return True
        else:
            return False

