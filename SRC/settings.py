import json

with open('JSON/settings.json', 'r') as f:
    settings = json.load(f)

    print(settings)

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
    "info1": informations["info1"]
}
