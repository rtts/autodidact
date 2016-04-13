import re
from django import template
from django.conf import settings
from ..models import *

register = template.Library()

@register.inclusion_tag('autodidact/include/editor.html', takes_context=True)
def autodidact_editor(context):
    context['edit_type'] = context['request'].resolver_match.view_name
    return context

@register.filter()
def upload_urls(string, session):
    '''Replaces filenames between [brackets] with a Markdown hyperlink to the correct uploads directory'''

    # Some people, when confronted with a problem, think "I know,
    # I'll use regular expressions."  Now they have two problems.
    # -- Jamie Zawinski
    pattern = re.compile('(?P<prefix>^|[^)\]])\[(?P<filename>[^\]]+)\](?P<postfix>[^(\[]|$)')

    while True:
        match = pattern.search(string)
        if match:
            prefix = match.group('prefix')
            filename = match.group('filename')
            url = settings.MEDIA_URL + session.get_absolute_url()[1:] + filename
            postfix = match.group('postfix')
            markdown = '{prefix}[{filename}]({url}){postfix}'.format(
                filename = filename,
                url      = url,
                prefix   = prefix,
                postfix  = postfix,
            )
            string = pattern.sub(markdown, string)
        else:
            break

    return string
