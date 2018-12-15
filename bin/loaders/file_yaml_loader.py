import yaml

def get_data(path):
    with open(path, 'r') as stream:
        data = yaml.load(stream)
    return data
