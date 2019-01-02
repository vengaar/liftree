import yaml
import json
import os
import markdown
import datetime

UNKNOW = '?'

def filter_liftree_link(path):
    return f'<a href="/show?path={path}">{path}</a>'

def filter_timestamp_delta(begin, end):
    try:
        seconds = int(end-begin)
        date = str(datetime.timedelta(seconds=seconds))
    except:
        date = UNKNOW
    return date

def filter_seconds2duration(seconds):
    try:
        date = str(datetime.timedelta(seconds=int(seconds)))
    except:
        date = UNKNOW
    return date

def filter_timestamp2date(timestamp, format='%Y-%m-%d %H:%M:%S'):
    try:
        ts = int(timestamp)
        date = datetime.datetime.utcfromtimestamp(ts).strftime(format)
    except:
        date = UNKNOW
    return date

def filter_to_yaml(input):
    return yaml.dump(input, default_flow_style=False)

def filter_to_json(value):
    return json.dumps(value)

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

def filter_get(my_list, value, default=''):
    """
      Return value if present in list 
    """
    if my_list is None:
        return default
    else:
        return value if value in my_list else default
