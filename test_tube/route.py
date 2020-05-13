from wsgiref.headers import Headers
from http.client import responses

class Route():

    def __init__(self, path, method, callback, status=200, content_type='text/html; charset=UTF-8'):
        self.path = path
        self.method = method
        self.callback = callback

        self.__status = status
        self.__ct = content_type
        self.__header = Headers()

    @property
    def status_code(self):
        return '{} {}'.format(self.__status, responses[self.__status])

    @property
    def headers(self):
        self.__header.add_header('Strict-Transport-Security', 'max-age=31536000; includeSubDomains')
        self.__header.add_header('Content-Security-Policy', "default-src 'self'")
        self.__header.add_header('X-Content-Type-Options', 'nosniff')
        self.__header.add_header('X-Frame-Options', 'SAMEORIGIN')
        self.__header.add_header('X-XSS-Protection', '1; mode=block')
        self.__header.add_header('Content-type', self.__ct)
        return self.__header.items()

class Static(Route):

    def __init__(self, status, content_type):
        super().__init__(None, None, None, status = status, content_type=content_type)