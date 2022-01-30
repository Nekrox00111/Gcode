import json

file = open('config.json')
config_file = json.load(file)
file.close()

MACHINE_SETTINGS = config_file