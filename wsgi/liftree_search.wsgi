import traceback
import json

# liftree import
from liftree import *
from constants import *

def application(environ, start_response):

    search_formats = ('sui', 'raw')

    try:
        parameters = parse_qs(environ['QUERY_STRING'])
        _liftree = LifTree()
        raw_results = _liftree.search(parameters)
        format = parameters.get('format', ["raw"])[0]
        if format == 'sui':
            # @todo add format function
            formatted_results = [
                dict(
                    title=result,
                    url=f'/show?path={result}'
                )
                for result in raw_results.get('files', [])
            ]
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
