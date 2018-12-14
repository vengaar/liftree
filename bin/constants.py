from http import HTTPStatus

HTTP_200 = f'{HTTPStatus.OK.value} {HTTPStatus.OK.phrase}'
HTTP_500 = f'{HTTPStatus.INTERNAL_SERVER_ERROR.value} {HTTPStatus.INTERNAL_SERVER_ERROR.phrase}'

CONTENT_TYPE_HTML = 'text/html'
CONTENT_TYPE_TEXT = 'text/plain'
CONTENT_TYPE_JSON = 'application/json'
