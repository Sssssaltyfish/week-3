from urllib.parse import urlencode
from django import template

register = template.Library()

# Self-defined filters
@ register.filter
def sliceby(value, arg: int):
    length = len(value)
    step = int(arg)
    ret = []
    for i in range(length//step - 1):
        ret.append(value[i*step:(i+1)*step])
    else:
        ret.append(value[(i+1)*step:])
    return ret

@ register.filter
def urlarg(value: str):
    try:
        arg = value.split('?')[1]
        return f'?{arg}' if arg else ''
    except IndexError:
        return ''