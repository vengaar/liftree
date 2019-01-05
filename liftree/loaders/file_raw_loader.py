def get_data(path, params):
    with open(path, 'r', encoding='utf-8') as stream:
        data = stream.read()
    return data
