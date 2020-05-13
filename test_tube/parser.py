import re

from html import escape
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()

        self.__script = False

        self.__html = []

    def handle_starttag(self, tag, attrs):
        tag_opts = []
        for attr in attrs:
            attribute = attr[0]
            attribute_value = attr[1]
            if attribute in set(['href', 'src']) and not chek_url(attribute_value):
                attribute_value = 'bad_url'
            
            if 'on' in attribute:
                attribute=escape_script(attribute)
                attribute_value=escape_script(attribute_value)


            tag_opts.extend(' {}="{}"'.format(attribute, escape(attribute_value)))

        if tag == "script":
            self.__script = True

        start_tag = '<{}{}>'.format(tag, ''.join(tag_opts))

        self.__html.extend(start_tag)

    def handle_data(self, data):
        if self.__script :

            if '/script' in data:
                data = 'bad script'
            data = check_string_literal(data)
            self.__html.extend(data)
        else:
            self.__html.extend(escape(data))

    def handle_endtag(self, tag):
        if tag == "script":
            self.__script = False
        self.__html.extend('</{}>'.format(tag))

    @property
    def value(self):
        return ''.join(self.__html)

def chek_url(url):
    ok_url = ['github.com', 'kosh.dev', 'www.cript.me']

    if re.match('^\/', url) is not None:
        return True

    elif re.match('^https?://', url) is not None:
        for site_name in ok_url:
            if re.match('^https?://{}'.format(site_name), url) is not None:
                return True

    return False

def escape_script(script):
    words = list(script)
    word_list = []
    for word in words:
        if word in ['"', "'"]:
            word_list.extend('\{}'.format(word))
        else:
            word_list.extend(word)
    return ''.join(word_list)

def check_string_literal(data):
    data_list = []
    for line_data in data.splitlines():
        matchobj =  re.search('\(.+\)', line_data)
        if matchobj is not None:
            print(matchobj.group()[1:-1])
            matchobj = matchobj.group()[1:-1]
            if re.search('</', matchobj) is not None:
                line_data = line_data.replace(matchobj, "'bad literal'")
            else:
                line_data = line_data.replace(matchobj[1:-1], escape_script(matchobj[1:-1]))
        data_list.extend('{}\n'.format(line_data))

    return ''.join(data_list)