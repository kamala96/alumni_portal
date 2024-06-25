from django.conf import settings


def site_name(request):
    return {'site_name': settings.SITE_NAME}


def navigation_menu(request):
    main_menu = Navigationmenu.objects.filter(menu_type='main', is_active=True).order_by('order_id')
    return {'main_menu': main_menu}


# def menu_context(request):
#     # Retrieve all menu items
#     top_menus = Navigationmenu.objects.filter(parent_menu__isnull=True, is_visible=True)
#     return {'menus': top_menus}