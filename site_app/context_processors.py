from django.conf import settings
from site_app.models import *


def site_name(request):
    return {'site_name': settings.SITE_NAME}


# def menu_context(request):
#     # Retrieve all menu items
#     top_menus = Navigationmenu.objects.filter(parent_menu__isnull=True, is_visible=True)
#     return {'menus': top_menus}