import traceback
from cgi import parse_qs
from logging.config import fileConfig

# liftree import
import liftree
from liftree import LifTree
from liftree.utils import get_first_parameter

# Share liftre across requests
#_liftree = LifTree()

def application(environ, start_response):

    try:
        fileConfig('/etc/liftree/logging.conf')
        parameters = parse_qs(environ['QUERY_STRING'])
        path = get_first_parameter('path', parameters)
        renderer = get_first_parameter('renderer', parameters)
        _liftree = LifTree()
        status, content_type, output = _liftree.render(path, renderer)
    except:
        status = liftree.HTTP_500
        content_type = liftree.CONTENT_TYPE_TEXT
        trace = traceback.format_exc()
        output = trace.encode('utf-8')

    response_headers = [
        ('Content-type', content_type),
        ('Content-Length', str(len(output)))
    ]
    start_response(status, response_headers)
    return [output]
