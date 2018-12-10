import sys
import getpass
import pprint
import shutil

from constants import *

def application(environ, start_response):
    status = HTTP_200
    path = str(sys.path)
    user = getpass.getuser()
    data = dict(
        path=str(sys.path),
        environ=environ,
        user=getpass.getuser()
    )
    output = pprint.pformat(data).encode('utf-8')
    response_headers = [('Content-type', CONTENT_TYPE_TEXT),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers, sys.exc_info())
    return [output]
