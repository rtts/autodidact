from django import template
from ..models import *

register = template.Library()

@register.inclusion_tag('autodidact/include/editor.html', takes_context=True)
def autodidact_editor(context):
    context['edit_type'] = context['request'].resolver_match.view_name
    return context
