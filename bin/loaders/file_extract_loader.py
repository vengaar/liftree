import yaml

def get_data(path):
    "".startswith
    prefix = "### DOC ###"
    with open(path, 'r') as stream:
        data = [
            line[len(prefix):]
            for line in stream
            if line.startswith(prefix)
        ]
    return yaml.load("".join(data))
