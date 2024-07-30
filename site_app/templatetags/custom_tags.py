from django import template
from site_app.models import *
register = template.Library()
from site_app.models import TrafficLog
from django.utils import timezone
from datetime import timedelta



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
def get_social_media_slider(footer=False):
    if footer:
        return SocialMedia.objects.filter(is_on_footer=True, is_active=True)
    else:
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



@register.simple_tag
def get_footer_items(university=False):
    if university:
        return FooterLink.objects.filter(link_type='university', is_active=True)
    else:
        return FooterLink.objects.filter(link_type='useful', is_active=True)
    

@register.simple_tag
def get_filtered_news():
    return NewsPost.objects.filter(is_published=True).order_by('-created_at')[:2]


    


@register.filter
def truncate_chars(value, max_length):
    if len(value) <= max_length:
        return value
    else:
        truncated_value = value[:max_length]
        words = truncated_value.split(' ')
        words.pop() 
        return ' '.join(words) + '...'
    


@register.filter
def sort_by(queryset, order):
    return queryset.order_by(order)



@register.simple_tag
def get_alumni_traffic_statistics():
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=today_start.weekday())
    month_start = now.replace(day=1)
    year_start = now.replace(month=1, day=1)

    online_visits = TrafficLog.objects.filter(timestamp__gte=now - timedelta(minutes=5)).count()
    today_visits = TrafficLog.objects.filter(timestamp__gte=today_start).count()
    week_visits = TrafficLog.objects.filter(timestamp__gte=week_start).count()
    month_visits = TrafficLog.objects.filter(timestamp__gte=month_start).count()
    year_visits = TrafficLog.objects.filter(timestamp__gte=year_start).count()
    all_time_visits = TrafficLog.objects.all().count()

    desktop_visits = TrafficLog.objects.filter(device_type='desktop').count()
    mobile_visits = TrafficLog.objects.filter(device_type='mobile').count()
    tablet_visits = TrafficLog.objects.filter(device_type='tablet').count()
    other_visits = TrafficLog.objects.filter(device_type='other').count()

    return {
        'online_visits': online_visits,
        'today_visits': today_visits,
        'week_visits': week_visits,
        'month_visits': month_visits,
        'year_visits': year_visits,
        'all_time_visits': all_time_visits,
        'desktop_visits': desktop_visits,
        'mobile_visits': mobile_visits,
        'tablet_visits': tablet_visits,
        'other_visits': other_visits,
    }