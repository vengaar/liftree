import yaml
import json
import os
import markdown
import datetime
import jmespath

UNKNOW = '?'

def filter_file_stat(value):
    """
    """
    if os.path.isfile(value):
        return os.stat(value)
    else:
        return f'{value} is not a file'

def filter_json_query(data, expr):
    return jmespath.search(expr, data)

def filter_liftree_link(path, class_name=''):
    return f'<a class="{class_name}" href="/show?path={path}">{os.path.basename(path)}</a>'

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

def filter_to_yaml(value):
    try:
      result = yaml.dump(value, default_flow_style=False)
    except:
      result = value
    return result

def filter_to_json(value):
    return json.dumps(value)

def filter_to_markdown(value):
    extensions = ['extra', 'smarty']
    return markdown.markdown(value, extensions=extensions, output_format='html5')

def filter_dirname(path):
     return os.path.dirname(path)

def filter_basename(path):
     return os.path.basename(path)

def filter_get(my_list, value, default=''):
    """
      Return value if present in list 
    """
    if my_list is None:
        return default
    else:
        return value if value in my_list else default
