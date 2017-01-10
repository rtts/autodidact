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
def upload_urls(string, url):
    '''Replaces filenames between [brackets] with a Markdown hyperlink to the correct uploads directory'''

    # Some people, when confronted with a problem, think "I know,
    # I'll use regular expressions."  Now they have two problems.
    # -- Jamie Zawinski
    pattern = re.compile(r'\[\[(?P<filename>[^\]]+)\]\]')

    # Convert possible model instance to string
    string = str(string)

    while True:
        match = pattern.search(string)
        if match:
            filename = match.group('filename')
            url = settings.MEDIA_URL + url[1:] + filename
            html = '<a download href="{url}">{filename}</a>'.format(
                filename = filename,
                url = url,
            )
            string = string.replace(match.group(), html)
        else:
            break

    return mark_safe(string)
