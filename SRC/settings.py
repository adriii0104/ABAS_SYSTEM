import json

with open('settings.json', 'r') as f:
    settings = json.load(f)

    version = settings['app_settings']['version']
    name = settings['app_settings']['name']
    language = settings['app_settings']['language']
    license = settings['app_settings']['license']


    print(version)


APP_REQUERIMENTS = (
    version,
    name,
    language,
    license
)


USER_SESSION = {}


PYTHON_VERSION = "3.11.5 ABAS"