import yaml

def to_yaml(input):
    return yaml.dump(input, default_flow_style=False)
