from django import template
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
import markdown
from markdown.extensions import Extension

class EscapeHtml(Extension):
    def extendMarkdown(self, md, md_globals):
        del md.preprocessors['html_block']
        del md.inlinePatterns['html']

register = template.Library()

@register.filter(name='markdown', is_safe=True)
def convert_to_markdown(value):
    return mark_safe(markdown.markdown(force_unicode(value), extensions=[EscapeHtml(), 'smarty', 'tables']))
