import json

def load(path):
    with open(path, 'r') as stream:
        data = stream.read()
    return json.loads(data)
