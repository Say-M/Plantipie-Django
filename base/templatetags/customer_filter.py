from django import template

register = template.Library()

@register.filter()
def calculateDiscount(value,arg):
    return value - (( value * arg ) / 100 )
