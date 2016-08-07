import json

def get_credentials():
    path = 'ha_credentials.json'
    with open(path) as f:
        data = json.load(f)
        return data

