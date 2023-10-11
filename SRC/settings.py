import json
import os
from screeninfo import get_monitors

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
            "user_information": kwargs, "data":{
                "number_of_products": 0,
            }
        }, proccess, indent=4)
    with open("JSON/temporary.json", "r", encoding="utf-8") as proccess:
        loader = json.load(proccess)
        USER_SESSION["enterprise_name"] = loader["user_information"]["enterprise_name"]

def check_log():
    if os.path.exists("JSON/temporary.json"):
        with open("JSON/temporary.json", "r", encoding="utf-8") as check:
            checked = json.load(check)
            if not checked["user_information"]["logued"]:
                return False
            else:
                USER_SESSION["enterprise_name"] = checked["user_information"]["enterprise_name"]
                return True
    else:
        return False

monitor = get_monitors()

for monitores in monitor:
    width = monitores.width
    height = monitores.height