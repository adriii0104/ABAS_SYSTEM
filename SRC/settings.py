import json

with open('settings.json', 'r') as f:
    settings = json.load(f)


    version = settings['version']
    name = settings['name']
    language = settings['language']
    license = settings['license']


APP_REQUERIMENTS = (
    version,
    name,
    language,
    license
)


USER_SESSION = {}


PYTHON_VERSION = "3.11.5 ABAS"