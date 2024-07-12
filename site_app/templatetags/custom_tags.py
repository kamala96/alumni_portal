from django import template

from site_app.models import *


register = template.Library()



@register.simple_tag
def get_top_header_items(left=False):
    if left:
        return TopHeader.objects.filter(position=TopHeader.LEFT, is_active=True)
    else:
        return TopHeader.objects.filter(position=TopHeader.RIGHT, is_active=True)
    

@register.simple_tag
def get_navigation_menu(need_subMenus=False, parentMenu=None):
    if need_subMenus and parentMenu:
        # Get all subMenus by Parent Object or Parent ID/PK
        if isinstance(parentMenu, Navigationmenu):
            menus = Navigationmenu.objects.filter(parent=parentMenu, is_active=True)
        else:
            myObj = Navigationmenu.objects.get(pk=parentMenu)
            menus = Navigationmenu.objects.filter(parent=myObj, is_active=True).order_by('id')
    else:
        # Get Main/Root Menu only
        menus = Navigationmenu.objects.filter(parent__isnull=True, menu_type=Navigationmenu.MAIN_MENU_TYPE, is_active=True)
    return menus

@register.filter
def submenus(menu):
    return menu.submenus.filter(is_active=True).order_by('id')

# @register.simple_tag
# def get_navigation_menu():
#     return Navigationmenu.objects.filter(menu_type=Navigationmenu.MAIN_MENU_TYPE, is_active=True)



@register.simple_tag
def get_sliders():
    return Slider.objects.filter(is_slider_active=True)

@register.simple_tag
def get_social_media_slider():
    return SocialMedia.objects.filter(is_on_slider=True, is_active=True)



@register.filter
def display_menu(menu, user):
    if menu.slug in ['profile', 'logout', 'transcripts']:
        return user.is_authenticated
    elif menu.slug in ['login', 'register']:
        return not user.is_authenticated
    return True



@register.filter
def multiply(value, arg):
    return value * arg