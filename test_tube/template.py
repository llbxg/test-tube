import re

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
                        ("{%\s?elif\s(?P<value>.+?)\s?%}", self.handle_elif)
                      ]

    def process(self, _kws={}):
        for num, line in enumerate(self.lines):
            if line == '':
                continue

            for handle in self.handles:
                value = re.search(handle[0], line)

                if value is not None:
                    handle[1](num, value.groupdict()['value'], _kws)

            if not self.__if_bool:
                self.lines[num] = ''
        
    def handle_value(self, num, value, _kws={}):
        locals().update(_kws)
        self.lines[num] = self.lines[num].replace('{{%s}}'%value, eval(value))

    def handle_if(self, num, value, _kws={}):
        locals().update(_kws)
        if eval(value):
            self.__if_bool=True
            self.__elif_bool = False

        else:
            self.__if_bool=False
            self.__elif_bool = True

        self.lines[num] = ''
        
    
    def handle_elif(self, num, value, _kws={}):
        self.__if_bool=False
        locals().update(_kws)
        if self.__elif_bool:
            if eval(value):
                self.__if_bool=True
                self.__elif_bool = False
        self.lines[num] = ''

    def handle_endif(self, num, value, _kws={}):
        self.lines[num] = ''
        self.__if_bool=True

    @property
    def value(self):
        return ''.join(self.lines)
