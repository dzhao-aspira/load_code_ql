# configuration.py

import os 

def load_properties(file_path):
    properties = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                properties[key.strip()] = value.strip()
    return properties

file_path = os.path.join(os.path.dirname(__file__), 'config.properties')

config = load_properties(file_path)


def getOwner():
    return config.get('org')

def getDay():
    return int(config.get('days'))

def getToken():
    token = os.getenv('GIT_API_KEY')
    return token
