from django import template
from django.urls import NoReverseMatch
from django.core.urlresolvers import reverse

try:
    # Wagtail 2 & Python 3
    from urllib.parse import unquote_plus
    from wagtail.core.models import Page
except ImportError:
    # Wagtail 1.x & Python 2
    from urllib import unquote_plus
    from wagtail.wagtailcore.models import Page

register = template.Library()


@register.inclusion_tag('wagtailerrorpages/fragments/404message.html', takes_context=True)
def message404(context, max_results=5):
    url_path = context['request'].path_info
    search_query = unquote_plus(url_path).replace('/', ' ')
    search_results = Page.objects.live().public().search(search_query)[0:max_results]
    search = True

    try:
        # Some sites may not have search.
        reverse('search')
    except NoReverseMatch:
        search = False

    return {
        'search': search,
        'search_query': search_query,
        'search_results': search_results,
    }
