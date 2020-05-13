import os
from html import escape
from html.parser import HTMLParser
from string import Template

from test_tube.parser import MyHTMLParser


def open_file(path, ro='rb'):
    with open(path, ro) as data:
        data = data.read()
        return data

def open_img(file_name):
    return [open_file(os.path.join(os.path.abspath('.'), 'public/media', file_name))]

def open_template(file_name,d=None):
    for key in d:
        d[key] = escape(d[key])

    path = os.path.join(os.path.abspath('.'), 'templates/', file_name)
    data = open_file(path, 'r')
    template = Template(data)

    parser = MyHTMLParser()
    parser.feed(template.substitute(d))
    parser.close()

    return [parser.value.encode('utf-8')]