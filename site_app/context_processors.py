from django.conf import settings
from site_app.models import Navigationmenu


def site_name(request):
    return {'site_name': settings.SITE_NAME}


def navigation_menu(request):
    main_menu = Navigationmenu.objects.filter(menu_type='main', is_active=True).order_by('order_id')
    return {'main_menu': main_menu}
