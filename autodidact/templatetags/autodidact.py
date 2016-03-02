from django import template
from ..models import *

register = template.Library()

@register.inclusion_tag('autodidact/navigation.html', takes_context=True)
def autodidact_navigation(context):
    return context

@register.inclusion_tag('autodidact/editor.html', takes_context=True)
def autodidact_editor(context):
    return context
