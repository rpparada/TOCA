from django import template

register = template.Library()

@register.filter
def determinatag(value):
    print('hola :'+value)
    return 'hot'
