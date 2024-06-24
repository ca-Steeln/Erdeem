
from django import template
from settings.forms import SessionLanguageForm
from search.forms import SearchForm

register = template.Library()

@register.inclusion_tag('tags/language_tag.html', takes_context=True)
def render_language_selector(context):
    return {'language_form': SessionLanguageForm()}


@register.inclusion_tag('tags/search_tag.html', takes_context=True)
def render_search_input(context):
    return {'search_form': SearchForm()}