import re
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from ..models import *

register = template.Library()

@register.simple_tag
def autodidact_version():
    try:
        import autodidact
        return autodidact.__version__
    except ImportError:
        return 'unknown'

@register.simple_tag
def bps_version():
    try:
        import bps
        return bps.__version__
    except ImportError:
        return 'unknown'

@register.inclusion_tag('autodidact/include/editor.html', takes_context=True)
def autodidact_editor(context):
    context['edit_type'] = context['request'].resolver_match.view_name
    return context

@register.filter()
def upload_urls(string):
    '''Replaces filenames between [[square brackets]] with a hyperlink'''
    return substitute(string, r'\[\[(?P<filename>[^\]]+)\]\]', '<a download href="{url}">{filename}</a>')

@register.filter()
def insert_images(string):
    '''Replaces filenames between {{curly brackets}} with an HTML <img> tag'''
    return substitute(string, r'\{\{(?P<filename>[^\}]+)\}\}', '<img src="{url}" alt="{filename}">')

def substitute(string, regexp, subst):
    '''Searches the string for the filename as formatted in the regular expression. Substitutes it with `subst`.'''

    # Some people, when confronted with a problem, think "I know,
    # I'll use regular expressions."  Now they have two problems.
    # -- Jamie Zawinski
    pattern = re.compile(regexp)

    # Convert possible model instance to string
    string = str(string)

    while True:
        match = pattern.search(string)
        if match:
            filename = match.group('filename')
            url = settings.MEDIA_URL + filename
            html = subst.format(
                filename = filename,
                url = url,
            )
            string = string.replace(match.group(), html)
        else:
            break

    return mark_safe(string)
