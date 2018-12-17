import yaml
import json

def filter_to_yaml(input):
    return yaml.dump(input, default_flow_style=False)

def filter_flat(default, sep=','):
    if default is None:
        return ''
    elif isinstance(default, list):
        return sep.join(default)
    else:
        return default

def filter_selected_options(value):
    if value is None:
        selected_options = []
    elif isinstance(value, list):
        selected_options = [
            dict(name=option, value=option, selected=True)
            for option in value
        ]
    else:
        selected_options = [dict(name=value, value=value, selected=True)]
    return json.dumps(selected_options)

def filter_get(my_list, value):
    if my_list is None:
        return ''
    else:
        return value if value in my_list else ''
