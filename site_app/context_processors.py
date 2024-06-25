from django.conf import settings
<<<<<<< HEAD
from .models import *
=======

>>>>>>> 0ce97b92f9ae0e532dbfdf0a5877896f27732f30

def site_name(request):
    return {'site_name': settings.SITE_NAME}

def top_header(request):
    left_items = TopHeader.objects.filter(position=TopHeader.LEFT, is_active=True)
    right_items = TopHeader.objects.filter(position=TopHeader.RIGHT, is_active=True)
    return {
        'left_items': left_items,
        'right_items': right_items
    }


def navigation_menu(request):
    main_menu = Navigationmenu.objects.filter(menu_type='main', is_active=True).order_by('order_id')
    return {'main_menu': main_menu}


# def menu_context(request):
#     # Retrieve all menu items
#     top_menus = Navigationmenu.objects.filter(parent_menu__isnull=True, is_visible=True)
#     return {'menus': top_menus}