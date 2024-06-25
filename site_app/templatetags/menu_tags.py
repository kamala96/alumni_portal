from django import template
from site_app.models import Navigationmenu

register = template.Library()

@register.filter
def submenus(menu):
    return menu.submenus.filter(is_active=True).order_by('id')
