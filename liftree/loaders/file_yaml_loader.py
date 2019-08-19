import yaml

def get_data(path, params):
    with open(path, 'r') as stream:
        data = yaml.safe_load(stream)
    return data
