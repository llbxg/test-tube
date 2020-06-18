from http.client import responses
from functools import partial

from test_tube.file  import open_template
from test_tube.route import Route

def res_(code, env):
    if type(code)!=str:
        code = str(code)
    return ['{} : {}'.format(code, responses(code)).encode('utf-8')]

def res(status):
    return Route(None, None, partial(res_, status), status=status)