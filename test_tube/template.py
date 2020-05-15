import re

#from test_tube.file import open_file

class MyTemplate():

    def __init__(self, body):
        self.__html=[]
        body = body.replace('\r\n', '\n')
        self.lines = body.split('\n')
        self.__if_bool = True
        self.__elif_bool = False
        self.handles =[
                        ("{{(?P<value>.+?)}}", self.handle_value),
                        ("{%\s?if\s(?P<value>.+?)\s?%}", self.handle_if),
                        ("{%\s?endif(?P<value>.+?)\s?%}", self.handle_endif),
                        ("{%\s?elif\s(?P<value>.+?)\s?%}", self.handle_elif),
                        ("{%\s?else(?P<value>.+?)\s?%}", self.handle_else)
                      ]
        self.__html = []
    
    def including(self, _kws={}):
        for num, line in enumerate(self.lines):
            value = re.search("{%\s?include\s(?P<value>.+?)\s?%}", line)
            if value is not None:
                print(value)
                self.handle_include(num, value.groupdict()['value'], _kws)
                self.lines[num] = ''

            self.__html.extend([self.lines[num]])

    def process(self, _kws={}):
        for num, line in enumerate(self.__html):
            if line == '':
                continue

            for handle in self.handles:
                value = re.search(handle[0], line)

                if value is not None:
                    handle[1](num, value.groupdict()['value'], _kws)

            if not self.__if_bool:
                self.__html[num] = ''

    def handle_value(self, num, value, _kws={}):
        locals().update(_kws)
        kw = eval(value)
        if kw != str:
            kw = str(kw)
        self.__html[num] = self.__html[num].replace('{{%s}}'%value, kw)

    def handle_if(self, num, value, _kws={}):
        locals().update(_kws)
        if eval(value):
            self.__if_bool=True
            self.__elif_bool = False

        else:
            self.__if_bool=False
            self.__elif_bool = True

        self.__html[num] = ''

    def handle_elif(self, num, value, _kws={}):
        self.__if_bool=False

        if self.__elif_bool:
            locals().update(_kws)
            if eval(value):
                self.__if_bool=True
                self.__elif_bool = False

        self.__html[num] = ''

    def handle_endif(self, num, value, _kws={}):
        self.__html[num] = ''
        self.__if_bool=True
        self.__elif_bool = False

    def handle_else(self, num, value, _kws={}):
        self.__if_bool=False
        if self.__elif_bool:

            self.__if_bool=True
            self.__elif_bool = False
        self.__html[num] = ''

    def handle_include(self, num, value, _kws={}):
        data = open_file(eval(value), ro='r').replace('\r\n', '\n').split('\n')
        self.__html.extend(data)

    @property
    def value(self):
        return ''.join(self.__html)