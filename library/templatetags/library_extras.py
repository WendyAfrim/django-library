from datetime import date
from django import template

register = template.Library()

@register.filter
def days_left(date):
    d0 = date.today()
    d1 = date
    delta = d1 - d0
    return delta.days
