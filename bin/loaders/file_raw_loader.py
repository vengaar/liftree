def get_data(path, params):
    with open(path, 'r') as stream:
        data = stream.read()
    return data
