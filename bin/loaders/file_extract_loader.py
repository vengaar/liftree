import yaml

def get_data(path, params):
    prefix = params.get('prefix')
    format = params.get('format')
    # print(params)
    with open(path, 'r') as stream:
        lines = [
            line[len(prefix):]
            for line in stream
            if line.startswith(prefix)
        ]
    data = "".join(lines)
    if format == 'yaml':
        return yaml.load("".join(data))
    else:
        return data
