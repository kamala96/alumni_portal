from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

class TopHeader(models.Model):
    LEFT = 'left'
    RIGHT = 'right'
    MENU_POSITION_CHOICES = [
        (LEFT, 'Left'),
        (RIGHT, 'Right'),
    ]
    
    INTERNAL = 'internal'
    EXTERNAL = 'external'
    LINK_TYPE_CHOICES = [
        (INTERNAL, 'Internal'),
        (EXTERNAL, 'External'),
    ]
    
    MenuFor = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)
    link_type = models.CharField(max_length=8, choices=LINK_TYPE_CHOICES)
    link = models.URLField(blank=True, null=True)
    icon_class = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(
        max_length=5,
        choices=MENU_POSITION_CHOICES,
        default=RIGHT,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.link_type == self.INTERNAL and not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Navigationmenu(models.Model):
    MAIN_MENU_TYPE = 'main'
    SUB_MENU_TYPE = 'sub'
    MENU_TYPE_CHOICES = [
        (MAIN_MENU_TYPE, 'Main/Root Menu'),
        (SUB_MENU_TYPE, 'Sub Menu'),
    ]

    LINK_TYPE_CHOICES = [
        ('internal', 'Internal'),
        ('external', 'External'),
    ]

    menu_name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    link_type = models.CharField(max_length=8, choices=LINK_TYPE_CHOICES)
    link = models.URLField(blank=True, null=True)  # Required link field
    menu_type = models.CharField(max_length=4, choices=MENU_TYPE_CHOICES)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='submenus',
        limit_choices_to={'menu_type': MAIN_MENU_TYPE}
    )
    order_id = models.PositiveIntegerField(null=True, blank=True)
    icon_class = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    indentation = models.PositiveIntegerField(editable=False)

    def clean(self):
        if self.menu_type == 'sub' and self.parent is None:
            raise ValidationError('Sub menus must have a parent main menu.')
        if self.menu_type == 'main' and self.parent is not None:
            raise ValidationError('Main menus cannot have a parent menu.')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.menu_name)
        self.indentation = 0 if self.menu_type == 'main' else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.menu_name

    class Meta:
        ordering = ['order_id']
        

class ASiteSettings(models.Model):
    site_name = models.CharField(max_length=50, blank=True, null=True)
    icon_class = models.CharField(max_length=50, blank=True, null=True)
    main_logo = models.ImageField(upload_to='images/logo/', blank=True, null=True)
    favourite_icon = models.ImageField(upload_to='images/favicon/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Site Setting"




class EventCategory(models.Model):
    EVENT_CATEGORY_NAME_CHOICES = (
        ('current', 'Current Events'),
        ('recent', 'Recent Events'),
    )
    name = models.CharField(max_length=100, unique=True, choices=EVENT_CATEGORY_NAME_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name.upper()

    class Meta:
        verbose_name = "Event Category"
        verbose_name_plural = "Event Categories"
        ordering = ['name']


class Organizer(models.Model):
    ORGANIZER_NAME = (
        ('nit', 'National Institute Of Transport'),
        ('hidden', 'Other'),
    )
    name = models.CharField(max_length=100, unique=True, choices=ORGANIZER_NAME)
    description = models.TextField()
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name.upper()



class EventsPost(models.Model):
    title = models.CharField(max_length=200)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE, related_name='event_organizer', null=True, blank=True)
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE, related_name='event_posts')
    slug = models.SlugField(unique=True, max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    image = models.ImageField(upload_to='images/event/', blank=True, null=True)
    is_published = models.BooleanField(default=False, help_text='Whether it is publishable or not')
    is_published_on_slider = models.BooleanField(default=False, help_text='Whether it is publishable or not on the Slider')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title.upper()

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Event Post"
        verbose_name_plural = "Event Posts"



class NewsCategory(models.Model):
    NEWS_CATEGORY_NAME_CHOICES = (
        ('current', 'Current News'),
        ('recent', 'Recent News'),
    )
    name = models.CharField(max_length=100, unique=True, choices=NEWS_CATEGORY_NAME_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name.upper()

    class Meta:
        verbose_name = "News Category"
        verbose_name_plural = "News Categories"
        ordering = ['name']


class NewsPost(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    slug = models.SlugField(unique=True, max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='images/blog/', blank=True, null=True)
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE, related_name='news_posts')
    is_published = models.BooleanField(default=False, help_text='Whether it is publishable or not')
    is_published_on_slider = models.BooleanField(default=False, help_text='Whether it is publishable or not on the Slider')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title.upper()

    class Meta:
        ordering = ['-created_at']
        verbose_name = "News Post"
        verbose_name_plural = "News Posts"




class JobCategory(models.Model):
    JOB_CATEGORY_NAME_CHOICES = (
        ('internal', 'Internal Job'),
        ('external', 'External Job'),
    )
    name = models.CharField(max_length=100, unique=True, choices=JOB_CATEGORY_NAME_CHOICES)
    description = models.TextField(blank=True, null=True)
    #created_at = models.DateTimeField(auto_now_add=True)
    def _str_(self):
        return self.name.upper()

class JobPosting(models.Model):
    company_name = models.CharField(max_length=255)
    company_logo = models.ImageField(upload_to='images/job/', blank=True, null=True)
    job_title = models.CharField(max_length=255)
    job_description = models.TextField()
    alumni_provider = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='job_postings')
    job_deadline_date = models.DateField()
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True, related_name='job_category')
    job_location = models.CharField(max_length=255, blank=True, null=True)
    employment_type = models.CharField(max_length=50, choices=[
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Internship', 'Internship'),
        ('Contract', 'Contract'),
        ('Temporary', 'Temporary'),
        ('Volunteer', 'Volunteer'),
    ])
    salary_range = models.CharField(max_length=50, blank=True, null=True)
    required_qualifications = models.TextField(blank=True, null=True)
    preferred_qualifications = models.TextField(blank=True, null=True)
    responsibilities = models.TextField(blank=True, null=True)
    benefits = models.TextField(blank=True, null=True)
    application_procedure = models.TextField(blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    external_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.job_title.upper()
    


class FooterLink(models.Model):
     LINK_TYPE_CHOICES = [ ('university', 'University'), ('useful', 'Useful Link'), ]
     name = models.CharField(max_length=100)
     link_type = models.CharField(max_length=20, choices=LINK_TYPE_CHOICES) 
     url = models.URLField(max_length=255) 
     is_active = models.BooleanField(default=True) 
     is_for_newtab = models.BooleanField(default=False) 
     created = models.DateTimeField(auto_now_add=True) 
     updated = models.DateTimeField(auto_now=True)
     def _str_(self): 
         return f"{self.name} ({self.get_link_type_display()})"
     

class SocialMedia(models.Model): 
    name = models.CharField(max_length=100) 
    icon_class = models.CharField(max_length=100) 
    url = models.URLField(max_length=255) 
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True) 
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def _str_(self): 
        return self.name
    
    
class Responsibility(models.Model): 
    title = models.CharField(max_length=255) 
    desc = models.TextField()
    image = models.ImageField(upload_to='responsibilities/') 
    icon_class = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True) 
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def _str_(self): 
        return self.title


class Slider(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='static/images/slider/')
    description = models.TextField(blank=True, null=True)
    button_text = models.CharField(max_length=50, blank=True, null=True)
    button_link = models.URLField(blank=True, null=True)
    slider_link = models.URLField(blank=True, null=True)
    show_button = models.BooleanField(default=False)
    show_title = models.BooleanField(default=True)
    show_description = models.BooleanField(default=True)
    is_slider_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
