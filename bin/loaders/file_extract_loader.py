import yaml

def get_data(path, pattern='### DOC ###', format='yaml'):
    prefix = "### DOC ###"
    with open(path, 'r') as stream:
        data = [
            line[len(prefix):]
            for line in stream
            if line.startswith(pattern)
        ]
    if format == 'yaml':
        return yaml.load("".join(data))
    else:
        return data
