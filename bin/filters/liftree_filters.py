import yaml
import json
import os
import markdown

def filter_to_yaml(input):
    return yaml.dump(input, default_flow_style=False)

def filter_to_markdown(value):
    extensions = ['extra', 'smarty']
    return markdown.markdown(value, extensions=extensions, output_format='html5')

def filter_basename(path):
     return os.path.basename(path)


def filter_flat(default, sep=','):
    if default is None:
        return ''
    elif isinstance(default, list):
        return sep.join(default)
    else:
        return default

def filter_to_sui_options(value, selected=False):
    if value is None:
        selected_options = []
    elif isinstance(value, list):
        selected_options = [
            dict(name=option, value=option, selected=selected)
            for option in value
        ]
    else:
        selected_options = [dict(name=value, value=value, selected=selected)]
    return json.dumps(selected_options)
