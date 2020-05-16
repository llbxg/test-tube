import os
from html import escape
from html.parser import HTMLParser
from string import Template

from test_tube.parser import MyHTMLParser
from test_tube.template import MyTemplate
from test_tube.tools import open_file

def open_img(file_name):
    return [open_file(os.path.join(os.path.abspath('.'), 'public/media', file_name))]

def open_css(file_name):
    return [open_file(os.path.join(os.path.abspath('.'), 'public/css', file_name))]

def open_template(file_name,d=None):

    path = os.path.join(os.path.abspath('.'), 'templates/', file_name)
    data = open_file(path, 'r')

    template = Template(data)
    template = MyTemplate(data)
    template.including()
    template.process(d)

    parser = MyHTMLParser()
    parser.feed(template.value)
    parser.close()

    return [parser.value.encode('utf-8')]