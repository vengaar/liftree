import traceback

# liftree import
from liftree import *
from constants import *

def application(environ, start_response):

    try:
        parameters = parse_qs(environ['QUERY_STRING'])
        _liftree = LifTree()
        status, content_type, output = _liftree.render(parameters)
    except:
        status = HTTP_500
        content_type = CONTENT_TYPE_TEXT
        trace = traceback.format_exc()
        output = trace.encode('utf-8')

    response_headers = [
        ('Content-type', content_type),
        ('Content-Length', str(len(output)))
    ]
    start_response(status, response_headers)
    return [output]
