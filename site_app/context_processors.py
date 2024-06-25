from django.conf import settings
<<<<<<< HEAD
from site_app.models import Navigationmenu
=======
<<<<<<< HEAD
from .models import *
=======
>>>>>>> 121dc4c1a053ece313e228b40272a0ae323797cd

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
