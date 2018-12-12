import traceback
import json

# liftree import
from liftree import *
from constants import *
from utils import format_search_results_for_sui

def application(environ, start_response):

    search_formats = ('sui', 'raw')

    try:
        parameters = parse_qs(environ['QUERY_STRING'])

        query = parameters.get('query', [''])[0]
        by_cat = parameters.get('by_cat', ["false"])[0]
        _liftree = LifTree()
        raw_results = _liftree.search(query)
        format = parameters.get('format', ["raw"])[0]
        if format == 'sui':
            formatted_results = format_search_results_for_sui(raw_results['files'])
            output = dict(results=formatted_results)
        else:
            output = raw_results
        status = HTTP_200
        content_type = CONTENT_TYPE_JSON
        output = json.dumps(output)
        output = output.encode('utf-8')
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
