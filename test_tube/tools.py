import re

def open_file(path, ro='rb'):
    with open(path, ro) as data:
        data = data.read()
        return data

alphaReg = re.compile(r'^[a-zA-Z]+$')
def isalpha(s):
    return alphaReg.match(s) is not None