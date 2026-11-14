from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def pagination_url(context, page):
    params = context["request"].GET.copy()
    params["page"] = page
    return f"?{params.urlencode()}"
