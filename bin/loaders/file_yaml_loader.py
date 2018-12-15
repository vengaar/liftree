import yaml

def load(path):
    with open(path, 'r') as stream:
        data = yaml.load(stream)
    return data
