import json

def get_data(path):
    with open(path, 'r') as stream:
        data = stream.read()
    return json.loads(data)
