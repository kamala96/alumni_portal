from itertools import chain
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from site_app.models import *


def index(request):
    events = EventsPost.objects.filter(is_published=True, is_published_on_slider=True).order_by('-created_at') #[:6]
    news = NewsPost.objects.all() 
    responsibilitys = Responsibility.objects.all()
    jobs = JobPosting.objects.all()
    alumni_members = AlumniProfile.objects.all()

    about_us = []

    try:
        about_us = AboutUs.objects.get(is_active=True)
    except AboutUs.DoesNotExist:
        pass

    for event in events:
        event.item_type = 'Upcoming Events'
    for news_item in news:
        news_item.item_type = 'Current News'

    combined_posts = list(chain(events, news))


    context = {
        'combined_posts': combined_posts,
        'events': events,
        'news': news.filter(is_published=True, is_published_on_slider=True).order_by('-created_at'), #[:6]
        'all_news': news.filter(is_published=True).order_by('-created_at'), #[:6]
        'responsibilitys': responsibilitys.filter(is_active=True).order_by('-created'), #[:6]
        'jobs': jobs.filter(is_active=True).order_by('-created_at'), #[:6]
        'about_us': about_us,
        'total_alumni_member': alumni_members.filter(user__is_active=True).count,
    }
    return render(request, 'index.html', context)



def default_error_page(request):
    return render(request, 'errors/error404.html', status=404)


def handle_nav_menu_click(request, menu_slug):
    try:
        nav_menu = Navigationmenu.objects.get(slug=menu_slug)
    except Navigationmenu.DoesNotExist:
        return redirect('default_error_page')
    
    # about_us = []

    try:
        about_us = AboutUs.objects.get(is_active=True)
    except AboutUs.DoesNotExist:
        pass
    
    events = EventsPost.objects.all() 
    news = NewsPost.objects.all()
    jobs = JobPosting.objects.all()
    committees = AlumniCommittee.objects.all()
    alumni_speechs = AlumniSpeech.objects.all()
    alumni_members = AlumniProfile.objects.all()
    
    template_name = '_default.html'
    
    if nav_menu.slug in ['home']: 
        return redirect('index')

    elif nav_menu.slug in ['about']:
        template_name = 'about.html'

    elif nav_menu.slug in ['event']: 
        template_name = 'event.html'

    elif nav_menu.slug in ['gallery']:
        template_name = 'gallery.html'

    elif nav_menu.slug in ['contact']:
        template_name = 'contact.html'

    elif nav_menu.slug in ['news']:
        template_name = 'news.html'

    elif nav_menu.slug in ['job']:
        template_name = 'job.html'
    
    elif nav_menu.slug in ['committee']:
        template_name = 'committee.html'

    elif nav_menu.slug in ['directory']:
        template_name = 'directory.html'
        
        
    context = {
        'nav_menu': nav_menu,
        'events': events.filter(is_published=True).order_by('-created_at'), #[:6]
        'news': news.filter(is_published=True).order_by('-created_at'), #[:6]
        'jobs': jobs.filter(is_active=True).order_by('-created_at'), #[:6]
        'about_us': about_us,
        'committees': committees.filter(is_active=True).order_by('-order_id'), #[:5], about
        'all_committees': committees.filter(is_active=True).order_by('-order_id'), #[:5], committee garally
        'alumni_speechs': alumni_speechs.filter(is_published=True).order_by('-order_id'), #[:5],
        'alumni_members': alumni_members.filter(user__is_active=True).order_by('-graduation_year'),
        'total_alumni_member': alumni_members.filter(user__is_active=True).count,
    }

    return render(request, f'nav_menus/{template_name}', context)


def handle_event_click(request, event_id):
    # event = get_object_or_404(Event, pk=event_id)

    context = {
        # 'event': event
    } 
    return render(request, 'pages/event_details.html', context)

def handle_news_click(request, news_id):
    # posts = Post.objects.all()

    # news = get_object_or_404(Post, pk=news_id)
    # quick_links = QuickLink.objects.all()

    context = {
        # 'news': news,
        # 'latest_news': posts.filter(post_type='B').order_by('-created_at')[:4],
        # 'quick_links_a': quick_links.filter(group='A')[:7],
    }

    return render(request, 'pages/news_details.html', context)
