from django import template
from urllib.parse import urlencode

register = template.Library()

@register.inclusion_tag('includes/pagination_with_filter.html', takes_context=True)
def render_pagination(context, page_obj, per_page=10, add_url='#'):
    request = context['request']
    query_params = request.GET.copy()

    # Remove pagination-specific keys
    query_params.pop('page', None)
    query_params.pop('per_page', None)

    query_string = '&' + urlencode(query_params)

    return {
        'page_obj': page_obj,
        'per_page': int(request.GET.get('per_page', per_page)),
        'query_string': query_string,
        'add_url': add_url,
    }

