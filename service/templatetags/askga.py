from django import template
from django.core.cache import cache

register = template.Library()

cache.set('users', ['aaa', 'bbb'])

@register.inclusion_tag('inc/users_rating.html')
def rating():
    return {'users': cache.get('users')}