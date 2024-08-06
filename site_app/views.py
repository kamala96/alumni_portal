from itertools import chain
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from site_app.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from rest_framework.authtoken.models import Token
from datetime import datetime, timedelta, timezone
from django.contrib.auth import update_session_auth_hash
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db import transaction




def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = authenticate(request, username=username, password=password)
            user_username = User.objects.get(username=username)
            user_profile = User.objects.get(username=username).alumniprofile

            if user is not None and user.is_authenticated and (user_profile.lockout_until is None or user_profile.lockout_until <= timezone.now()):
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                reset_failed_login_attempts(user)
                return redirect(reverse('handle_nav_menu_click', args=['profile']))

            elif user is not None and user_profile.lockout_until is not None and user_profile.lockout_until > timezone.now() and user.alumniprofile.failed_login_attempts >= 3:
                remaining_time = user_profile.lockout_until - timezone.now()
                remaining_minutes = remaining_time.total_seconds() // 60
                messages.error(request, f"Your Account Has Been Temporarily Locked. Please Try Again Later!.")  #  Remaining Time: {remaining_minutes} Minutes
                return redirect(reverse('handle_nav_menu_click', args=['login']))
            else:
                increment_failed_login_attempts(user_username)
                messages.warning(request, f"Invalid Username Or Password. Please Try Again.")
                return redirect(reverse('handle_nav_menu_click', args=['login']))

        except:
            messages.warning(request, f"User Not Existing Or Invalid Account. Please Contact Admin.")
            return redirect(reverse('handle_nav_menu_click', args=['login']))

    else:
        return redirect(reverse('handle_nav_menu_click', args=['login']))




@login_required
def logout_view(request):
    request.session.flush()
    logout(request)
    messages.success(request, "Logout Successfully..")
    return redirect(reverse('handle_nav_menu_click', args=['login']))


def index(request):
    events = EventsPost.objects.all()
    news = NewsPost.objects.all() 
    responsibilitys = Responsibility.objects.all()
    jobs = JobPosting.objects.all()
    alumni_members = AlumniProfile.objects.all()
    gallarys = AlbumPhoto.objects.all()

    about_us = []
    alumni_month = AlumniOfTheMonth.objects.filter(is_active=True).first()

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
        'events': events.filter(is_published=True, is_published_on_slider=True).order_by('-created_at'), #[:6]
        'news': news.filter(is_published=True, is_published_on_slider=True).order_by('-created_at'),
        'all_news': news.filter(is_published=True).order_by('-created_at')[:3],
        'responsibilitys': responsibilitys.filter(is_active=True).order_by('-created')[:4],
        'jobs': jobs.filter(is_active=True).order_by('-created_at')[:6],
        'about_us': about_us,
        'total_alumni_member': alumni_members.filter(user__is_active=True).count(),
        'total_alumni_image': gallarys.filter(is_published=True).count(),
        'total_alumni_events': events.filter(is_published=True).count(),
        'gallarys': gallarys.filter(is_published=True).order_by('-uploaded_at')[:8],
        'alumni_month': alumni_month,
        'total_alumni_album': AlumniAlbum.objects.all().count()
    }
    return render(request, 'index.html', context)



def default_error_page(request):
    return render(request, 'errors/error404.html', status=404)



def handle_nav_menu_click(request, menu_slug):
    try:
        nav_menu = Navigationmenu.objects.get(slug=menu_slug)
    except Navigationmenu.DoesNotExist:
        return redirect('default_error_page')
    
    # member_profile = []
    

    if not request.user.is_authenticated:
        member_profile = None
    else:
        member_profile = AlumniProfile.objects.get(user=request.user)


    try:
        about_us = AboutUs.objects.get(is_active=True)
    except AboutUs.DoesNotExist:
        pass
    
    events = Paginator(EventsPost.objects.filter(is_published=True).order_by('-created_at'), 10)
    news = Paginator(NewsPost.objects.filter(is_published=True).order_by('-created_at'), 10)
    jobs = Paginator(JobPosting.objects.filter(is_active=True).order_by('-created_at'), 9)
    committees = AlumniCommittee.objects.all()
    alumni_speechs = AlumniSpeech.objects.all()
    alumni_members = Paginator(AlumniProfile.objects.filter(user__is_active=True).order_by('-graduation_year'), 15)
    alumni_album = Paginator(AlumniAlbum.objects.all().order_by('-created_at'), 3)

    page_number = request.GET.get('page')
    
    template_name = '_default.html'
    
    if nav_menu.slug in ['home']: 
        return redirect('index')
    
    elif nav_menu.slug in ['logout']:
        return redirect('user_logout')

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

    elif nav_menu.slug in ['transcripts']:
        template_name = 'transcripts.html'

    elif nav_menu.slug in ['directory']:
        template_name = 'directory.html'

    elif nav_menu.slug in ['register', 'login']:
        template_name = 'register.html'

    elif nav_menu.slug in ['profile']:
        template_name = 'user_account.html'

    elif nav_menu.slug in ['faqs']:
        template_name = 'faqs.html'
        
        
    context = {
        'nav_menu': nav_menu,
        'events': events.get_page(page_number),
        'news': news.get_page(page_number),
        'jobs': jobs.get_page(page_number),
        'about_us': about_us,
        'committees': committees.filter(is_active=True).order_by('order_id')[:8], #about
        'all_committees': committees.filter(is_active=True).order_by('order_id'), #[:5], committee garally
        'alumni_speechs': alumni_speechs.filter(is_published=True).order_by('-order_id'), #[:5],
        'alumni_members': alumni_members.get_page(page_number),
        'total_alumni_member': alumni_members.count,
        'albums': alumni_album.get_page(page_number),
        'AFFILIATION_CHOICES': AlumniProfile.AFFILIATION_CHOICES,
        'COURSE_CHOICES': AlumniProfile.COUSE_CHOICES,
        'DEPT_CHOICES': AlumniProfile.DEPARTIMENT_CHOICES,
        'GENDER_CHOICES': AlumniProfile.GENDER_CHOICES,
        'COMPAS': AlumniProfile.COMPAS_CHOICES,
        'SONIT_LEADER': AlumniProfile.SONIT_LEADER_CHOICES,
        'member_profile': member_profile,
        'faqs': AlumniFAQ.objects.filter(is_active=True).order_by('id'),
    }

    return render(request, f'nav_menus/{template_name}', context)


def handle_event_click(request, event_id):
    events = get_object_or_404(EventsPost, pk=event_id)

    context = {
        'events': events,
    } 
    return render(request, 'pages/event_details.html', context)

def handle_news_click(request, news_id):
    news = get_object_or_404(NewsPost, pk=news_id)
    comments = news.comment.filter(parent__isnull=True)
    new_comment = None
    total_comments = news.comment.count()

    if request.method == 'POST':
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')
        new_comment = Comment.objects.create(
            news=news,
            author=AlumniProfile.objects.get(id=request.user.id), 
            content=content,
            parent=Comment.objects.get(id=parent_id) if parent_id else None
        )
        return redirect('handle_news_click', news_id=news.id)

    context = {
        'news': news,
        'comments': comments,
        'total_comments': total_comments,
    }

    return render(request, 'pages/news_details.html', context)


def handle_album_click(request, album_id):
    albums = AlumniAlbum.objects.all()
    # albums = get_object_or_404(NewsPost, pk=album_id)

    context = {
        'albums': albums.filter(pk=album_id).order_by('-created_at'),
    }

    return render(request, 'pages/single_album.html', context)

@login_required
def handle_user_profile_click(request, user_id):
    single_member = get_object_or_404(AlumniProfile, pk=user_id)

    context = {
        'single_member': single_member,
    }

    return render(request, 'pages/user_profile.html', context)




def user_create_account(request):
    if request.method == 'POST':
        # Retrieve data from the form
        first_name = request.POST.get('f_name')
        last_name = request.POST.get('l_name')
        email = request.POST.get('email')
        gender = request.POST.get('register_gender')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        passing_year = request.POST.get('passing_year')
        phone_number = request.POST.get('phone')
        current_location = request.POST.get('location')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect(reverse('handle_nav_menu_click', args=['register']))
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different username.')
            return redirect(reverse('handle_nav_menu_click', args=['register']))

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered. Please use a different email.')
            return redirect(reverse('handle_nav_menu_click', args=['register']))

        if AlumniProfile.objects.filter(phone=phone_number).exists():
            messages.error(request, 'Phone number already registered. Please use a different phone number.')
            return redirect(reverse('handle_nav_menu_click', args=['register']))

        try:
            with transaction.atomic():
                user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                AlumniProfile.objects.create(
                    user=user,
                    graduation_year=passing_year,
                    gender=gender,
                    location=current_location,
                    phone=phone_number,
                )
                login(request, user)
                messages.success(request, "User account registered successfully!")
                return redirect(reverse('handle_nav_menu_click', args=['profile']))
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect(reverse('handle_nav_menu_click', args=['register']))
    
    else:
        return redirect('index')



@login_required
def alumni_update_profile(request):
    user = request.user
    try:
        profile = user.alumniprofile
    except AlumniProfile.DoesNotExist:
        profile = AlumniProfile(user=user)

    if request.method == 'POST':
        user.first_name = request.POST.get('f_name')
        user.last_name = request.POST.get('l_name')
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()

        profile.birthday = request.POST.get('birthday')
        profile.country = request.POST.get('country')
        profile.location = request.POST.get('location')
        profile.phone = request.POST.get('phone')
        profile.gender = request.POST.get('gender')
        profile.affiliation_type = request.POST.get('affiliation_type')
        profile.comments = request.POST.get('comments')

        if request.POST.get('affiliation_type') != 'Staff':
            profile.graduated_course = request.POST.get('graduated_course')
            profile.department = request.POST.get('dept')
            profile.batch_year = request.POST.get('batch_year')
            profile.compass = request.POST.get('compass')
            profile.graduation_year = request.POST.get('passing_year')

        profile.is_sonit_leader = 'is_sonit_leader' in request.POST
        if profile.is_sonit_leader:
            profile.sonit_leader_position = request.POST.get('sonit_leader_position')
        else:
            profile.sonit_leader_position = None

        profile.save()
        messages.success(request, "User account updated successfully!")
        return redirect(reverse('handle_nav_menu_click', args=['profile']))

    return redirect(reverse('handle_nav_menu_click', args=['profile']))



@login_required
def alumni_update_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('oldpassword')
        new_password = request.POST.get('newpassword')
        confirm_new_password = request.POST.get('confirmpassword')
        user = request.user

        # Check if the old password matches
        from django.contrib.auth.hashers import check_password
        if check_password(old_password, user.password):
            # Check if new password and confirm password match
            if new_password == confirm_new_password:
                # Set the new password
                user.set_password(new_password)
                user.save()

                # Update the session authentication hash to prevent logout
                update_session_auth_hash(request, user)

                messages.success(request, 'Your password has been updated successfully.')
                redirect(reverse('handle_nav_menu_click', args=['profile']))
            else:
                messages.error(request, 'New password and confirm password do not match.')
        else:
            messages.error(request, 'Invalid old password. Password not updated.')

    return redirect(reverse('handle_nav_menu_click', args=['profile']))






@login_required
def usre_profile_image(request):
    user = request.user
    try:
        alumni_profile = user.alumniprofile
    except AlumniProfile.DoesNotExist:
        alumni_profile = AlumniProfile(user=user)

    if request.method == 'POST':
        profile_image = request.FILES.get('profile_image')
        cover_image = request.FILES.get('cover_image')
        # alumni_profile, created = AlumniProfile.objects.get_or_create(user=user)

        if profile_image:
            # Open the uploaded image using Pillow
            image = Image.open(profile_image)

            # Resize the image to 128x128 pixels
            image = image.resize((128, 128))

            # Save the resized image back to the ImageField
            temp_file = BytesIO()
            image.save(temp_file, format='PNG')
            alumni_profile.profile_picture.save(profile_image.name, ContentFile(temp_file.getvalue()), save=False)
            alumni_profile.save()
        elif cover_image:
            # Open the uploaded image using Pillow
            image = Image.open(cover_image)

            # Resize the image to 128x128 pixels
            image = image.resize((800, 800))

            # Save the resized image back to the ImageField
            temp_file = BytesIO()
            image.save(temp_file, format='PNG')
            alumni_profile.cover_profile.save(cover_image.name, ContentFile(temp_file.getvalue()), save=False)
            alumni_profile.save()

    return redirect(reverse('handle_nav_menu_click', args=['profile']))





def add_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if Subscriber.objects.filter(email=email).exists():
            messages.error(request, 'Email already subscribed.')
        else:
            subscribed_user = Subscriber(email=email)
            subscribed_user.save()
            messages.success(request, 'You have successfully subscribed to news notifications.')

    return redirect(reverse('handle_nav_menu_click', args=['home']))


def notify_subscribers(news):
    if not news.is_published: # or news.created_at > timezone.now():
        return 
    
    subscribers = Subscriber.objects.filter(is_active=True)
    for subscriber in subscribers:
        subject = f"New News: {news.title}"
        html_message = render_to_string('email/email_main.html', {'news': news})
        plain_message = strip_tags(html_message)
        #send_mail(subject, plain_message, 'example@gmail.com', [subscriber.email], html_message=html_message)


def footer_social(request):
    social_medias = SocialMedia.objects.filter(is_on_footer=True)
    return render(request, 'footer.html', {'social_medias': social_medias})







def reset_failed_login_attempts(user):
    user_profile = get_object_or_404(AlumniProfile, user_id=user)
    user_profile.failed_login_attempts = 0
    user_profile.lockout_until = None
    user_profile.save()

def increment_failed_login_attempts(id):
    user_profile = get_object_or_404(AlumniProfile, user_id=id)
    user_profile.failed_login_attempts += 1
    if user_profile.failed_login_attempts == 3:
        user_profile.lockout_until = timezone.now() + timedelta(hours=24)

    user_profile.save()