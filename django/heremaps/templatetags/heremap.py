from django import template
from splunkdj.templatetags.tagutils import component_context
register = template.Library()
@register.inclusion_tag('splunkdj:components/component.html', takes_context=True)
def heremarkermap(context, id, *args, **kwargs):
    return component_context(context,"heremarkermap",id,"view","heremaps/heremarkermap",kwargs)

