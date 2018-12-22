import yaml

def get_data(path, params):
    with open(path, 'r') as stream:
        data = yaml.load(stream)
    return data
