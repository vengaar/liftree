def load(path):
    with open(path, 'r') as stream:
        data = stream.read()
    return data
