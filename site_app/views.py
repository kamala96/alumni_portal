from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from site_app.models import *


def index(request):
    # sliders = Slider.objects.order_by('-created_at')[:7]
    # sliders = Slider.objects.filter(is_active=True).order_by('-created_at')
    # accounting_officer = AccountingOfficer.load()

    context = {
    }
    return render(request, 'index.html', context)



def default_error_page(request):
    return render(request, 'errors/error404.html', status=404)


def handle_nav_menu_click(request, menu_slug):
    try:
        menu = Navigationmenu.objects.get(slug=menu_slug)
    except Navigationmenu.DoesNotExist:
        return redirect('default_error_page')
    
    if menu.slug in ['home']:
        return redirect('index')

    elif menu.slug in ['about']:
        template_name = 'about.html'

    elif menu.slug in ['event']:
        template_name = 'event.html'

    elif menu.slug in ['gallery']:
        template_name = 'gallery.html'

    elif menu.slug in ['contact']:
        template_name = 'contact.html'
        
    context = {
        'menu': menu,
    }

    return render(request, f'nav_menus/{template_name}', context)
