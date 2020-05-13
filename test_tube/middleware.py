import re
import os

from test_tube.tools import isalpha
from test_tube.route import Static
from test_tube.file  import open_img

class MyMiddleware(object):
    
    def __init__(self, app):
        self.app = app

    def __call__(self,env, start_response):
        print("Middleware")
        file_path=env['PATH_INFO']

        file_target = re.match('/static/(?P<file_name>\D+)/', file_path)

        if file_target is not None:
            file_dic = file_target.groupdict()
            file_name = file_dic['file_name']
            file_main_name = os.path.splitext(file_name)[0]
            file_extention = os.path.splitext(file_name)[1]
            
            if isalpha(file_main_name):

                if file_extention in ['.jpg', '.png']:
                    try:
                        static = Static(200, 'image/ '+file_extention[1:])
                        start_response(static.status_code, static.headers)
                        return open_img(file_name)

                    except FileNotFoundError:
                        print('No such file or directory')
                
                elif file_extention == '.css':
                    try:
                        static = Static(200, 'text/css; charset=UTF-8')
                        start_response(static.status_code, static.headers)
                        return open_img(os.path.join(os.path.abspath('.'), 'public/', file_name))

                    except FileNotFoundError:
                        print('No such file or directory')

        return self.app(env, start_response)