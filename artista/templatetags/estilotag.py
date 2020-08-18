from django import template

register = template.Library()

@register.filter
def replacewithspace(value, arg):
    return str(value).replace(arg, ' ')

@register.filter
def replacespacewith(value, arg):
    return str(value).replace(' ',arg)
