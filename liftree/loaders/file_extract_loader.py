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
    # print(data)
    if format == 'yaml':
        return yaml.safe_load("".join(data))
    else:
        return data
