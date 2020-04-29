from django import template
from django.utils.safestring import mark_safe
from urllib.parse import parse_qs, urlsplit, urlunsplit, urlencode
register = template.Library()

MAP_BASE_URL = 'https://duckduckgo.com/'


@register.filter()
def map_url(address):
    return f"{set_query_parameter(MAP_BASE_URL, 'q', address)}&ia=maps&iaxm=maps"


# https://stackoverflow.com/a/12897375


def set_query_parameter(url, param_name, param_value):
    """Given a URL, set or replace a query parameter and return the
    modified URL.

    >>> set_query_parameter('http://example.com?foo=bar&biz=baz', 'foo', 'stuff')
    'http://example.com?foo=stuff&biz=baz'

    """
    scheme, netloc, path, query_string, fragment = urlsplit(url)
    query_params = parse_qs(query_string)

    query_params[param_name] = [param_value]
    new_query_string = urlencode(query_params, doseq=True)

    return urlunsplit((scheme, netloc, path, new_query_string, fragment))
