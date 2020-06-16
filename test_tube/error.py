from functools import partial

from test_tube.file  import open_template
from test_tube.route import Route

def error_(code, env):
    if type(code)!=str:
        code = str(code)
    return open_template('template.html', {'tp':'error', 'name':code, 'va':''})

def response_error(status):
    return Route(None, None, partial(error_, status), status=status)