import re

from test_tube.route import Route, Static

def e404(env):
    return [b'404 Not Found']

class App():
    def __init__(self):
        self.routes = []
        self.__e404 =Route(None, None, e404, status=404)

    def registration(self, path, method, callback):
        new_path = '^/' + path + '$'
        self.routes.append(Route(new_path, method, callback))

    def match(self, path, method):
        for route in self.routes:
            matched = re.match(route.path, path)
            if matched is not None:
                return route
        return self.__e404

    def __call__(self, env, start_response):
        path = env['PATH_INFO'] or '/'
        method = env['REQUEST_METHOD'].upper()
        
        route = self.match(path, method)

        start_response(route.status_code,route.headers)

        callback = route.callback
        return callback(env)