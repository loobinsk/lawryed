from django import template

register = template.Library()


@register.filter(name='split')
def slpit_filter(value, arg):
    return value.split(arg)


@register.filter
def index(indexable, i):
    res = '******** Error: Index of bound ******'
    try:
        res = indexable[i]
    except:
        pass
    return res
