from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from .validators import *


class AlumniProfile(models.Model):
    DEPARTIMENT_CHOICES = (
        ('cct', 'Computing And Communication Technology'),
        ('lts', 'Logistic And Transport Study'),

    )
    COMPAS_CHOICES = (
        ('nit', 'Mabibo Compass (DSM)'),
        ('arusha', 'Arusha Compass'),
        ('lindi', 'Lindi Compass'),
    )
    SONIT_LEADER_CHOICES = (
        ('president', 'President'),
        ('vice-president', 'Vice President'),
    )

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    COUSE_CHOICES = (
        ('Short Course', 'Short Course'),
        ('Certificate', 'Certificate'),
        ('Diploma', 'Diploma'),
        ('Bachelor', 'Bachelor'),
        ("Master's", "Master's"),
        ('Exchange Program', 'Exchange Program'),
    )

    AFFILIATION_CHOICES = (
        ('Staff', 'Staff'),
        ('Student', 'Student'),
        ('Both', 'Staff and Former Student'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    year_from = models.PositiveIntegerField(default=2024)  # = batch year
    graduation_year = models.PositiveIntegerField(
        default=2024)  # = passing year
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=20, blank=True, null=True, choices=GENDER_CHOICES)
    compass = models.CharField(
        max_length=255, null=False, choices=COMPAS_CHOICES, help_text='Which Compass Belong ?')
    Entry_year = models.PositiveIntegerField(default=2024)
    department = models.CharField(
        max_length=255, null=False, choices=DEPARTIMENT_CHOICES, help_text='Which Departments Belong ?')
    batch_year = models.PositiveIntegerField(default=2024)
    is_sonit_leader = models.BooleanField(default=False)
    sonit_leader_position = models.CharField(
        max_length=255, choices=SONIT_LEADER_CHOICES, blank=True, null=True)
    phone = PhoneNumberField(region="TZ", unique=True, null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to='images/testimonial/', blank=True, null=True)
    cover_profile = models.ImageField(
        upload_to='images/cover/', blank=True, null=True)
    region = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    affiliation_type = models.CharField(
        max_length=255, null=True, blank=True, choices=AFFILIATION_CHOICES)
    location = models.CharField(
        max_length=255, null=True, blank=True)  # current location
    graduated_course = models.CharField(
        max_length=255, null=True, blank=True, choices=COUSE_CHOICES)
    complete_profile_status = models.PositiveIntegerField(default=0)
    failed_login_attempts = models.IntegerField(default=0)
    lockout_until = models.DateTimeField(null=True, blank=True)
    comments = models.TextField(
        max_length=255, blank=True, null=False, default='Where Professionals Meet')

    def __str__(self):
        # {self.user.username}
        return f'{self.user.first_name} - {self.user.last_name}'


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
    main_logo = models.ImageField(
        upload_to='images/logo/', blank=True, null=True)
    favourite_icon = models.ImageField(
        upload_to='images/favicon/', blank=True, null=True)
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
    name = models.CharField(max_length=100, unique=True,
                            choices=EVENT_CATEGORY_NAME_CHOICES)
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
    name = models.CharField(max_length=100, unique=True,
                            choices=ORGANIZER_NAME)
    description = models.TextField()
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name.upper()


class EventsPost(models.Model):
    STATUS = (
        ('active', 'Active'),
        ('in-active', 'In-Active'),
    )
    title = models.CharField(max_length=200)
    organizer = models.ForeignKey(
        Organizer, on_delete=models.CASCADE, related_name='event_organizer', null=True, blank=True)
    category = models.ForeignKey(
        EventCategory, on_delete=models.CASCADE, related_name='event_posts')
    slug = models.SlugField(unique=True, max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    image = models.ImageField(upload_to='images/event/', blank=True, null=True)
    is_published = models.BooleanField(
        default=False, help_text='Whether it is publishable or not')
    is_published_on_slider = models.BooleanField(
        default=False, help_text='Whether it is publishable or not on the Slider')
    audience = models.TextField(null=True, blank=True)
    event_location = models.CharField(null=True, blank=True, max_length=100)
    event_status = models.CharField(null=True, blank=True, max_length=100, choices=STATUS)
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
    name = models.CharField(max_length=100, unique=True,
                            choices=NEWS_CATEGORY_NAME_CHOICES)
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
    author = models.ForeignKey(
        AlumniProfile, on_delete=models.CASCADE, related_name='author')
    slug = models.SlugField(unique=True, max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='images/blog/', blank=True, null=True)
    category = models.ForeignKey(
        NewsCategory, on_delete=models.CASCADE, related_name='news_posts')
    # if error migrate with default admin id after remove default
    posted_by = models.ForeignKey(
        AlumniProfile, on_delete=models.CASCADE, related_name='posted_by')
    category = models.ForeignKey(
        NewsCategory, on_delete=models.CASCADE, related_name='news_posts')
    is_published = models.BooleanField(
        default=False, help_text='Whether it is publishable or not')
    is_published_on_slider = models.BooleanField(
        default=False, help_text='Whether it is publishable or not on the Slider')
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
    name = models.CharField(max_length=100, unique=True,
                            choices=JOB_CATEGORY_NAME_CHOICES)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def _str_(self):
        return self.name.upper()


class JobPosting(models.Model):
    company_name = models.CharField(max_length=255)
    company_logo = models.ImageField(
        upload_to='images/job/', blank=True, null=True)
    job_title = models.CharField(max_length=255)
    job_description = models.TextField()
    alumni_provider = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='job_postings')
    job_deadline_date = models.DateField()
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(
        JobCategory, on_delete=models.SET_NULL, null=True, related_name='job_category')
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
    LINK_TYPE_CHOICES = [('university', 'University'),
                         ('useful', 'Useful Link'), ]
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
    text_to_display = models.CharField(blank=True, null=True, max_length=200)
    icon_class = models.CharField(max_length=100)
    url = models.URLField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_on_slider = models.BooleanField(default=True)
    is_on_footer = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.name.upper()
    # ICONS
    # fab fa-facebook-f
    # fab fa-instagram
    # fab fa-twitter
    # fab fa-youtube
    # fab fa-linkedin-in


class Responsibility(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    image = models.ImageField(upload_to='images/responsibilities/')
    icon_class = models.CharField(max_length=100)
    url = models.URLField(max_length=255, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def _str_(self):
        return self.title


class Slider(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='images/slider/')
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
        return self.title.upper()

    class Meta:
        ordering = ['-created_at']


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AboutUs(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(
        null=True, blank=True)  # about us nit Alumni
    description_image = models.ImageField(
        upload_to='images/about-page/', null=True, blank=True)
    welcome_note = models.TextField(null=True, blank=True)
    welcome_note_image = models.ImageField(
        upload_to='images/misc/', null=True, blank=True)
    mission = models.TextField(blank=True, null=True)
    mission_image = models.ImageField(
        upload_to='images/about-page/', null=True, blank=True)
    vision = models.TextField(blank=True, null=True)
    vision_image = models.ImageField(
        upload_to='images/about-page/', null=True, blank=True)
    achivements = models.TextField(blank=True, null=True)
    achivements_image = models.ImageField(
        upload_to='images/about-page/', null=True, blank=True)
    icon_class = models.CharField(max_length=100, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.welcome_note.upper()


class AlumniCommittee(models.Model):
    ALUMNI_POSITION_CHOICES = (
        ('president', 'President'),
        ('vice-president', 'Vice President'),
        ('secretary', 'Secretary'),
        ('asistance-secretary', 'Asistance Secretary'),
        ('finance-member', 'Finance Member'),
        ('committee-member', 'Committee Member'),
        ('alumni-admin', 'Alumni Admin'),
    )

    fullname = models.ForeignKey(
        AlumniProfile, on_delete=models.CASCADE, related_name='alumni_fullname', null=False)
    year_from = models.PositiveIntegerField(default=2024)
    year_to = models.PositiveIntegerField(default=2024)
    alumni_position = models.CharField(
        max_length=255, choices=ALUMNI_POSITION_CHOICES, null=False)
    slug = models.SlugField(max_length=100, unique=True, null=True)
    # null required to False also we can use varidation later  "validators=[validate_alumni_committee_image],"
    committee_profile_picture = models.ImageField(
        upload_to='images/committee/', blank=True, null=True)
    is_active = models.BooleanField(default=False)
    order_id = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return f'{self.fullname.user.first_name.upper()} - {self.fullname.user.last_name.upper()}'


class AlumniSpeech(models.Model):
    publisher = models.ForeignKey(
        AlumniProfile, on_delete=models.CASCADE, related_name='alumni_publisher', null=False)
    speech = models.TextField()
    is_published = models.BooleanField(default=False)
    order_id = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return f'{self.publisher.user.first_name.upper()} - {self.publisher.user.last_name.upper()}'


class AlumniAlbum(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.title.upper()


class AlbumPhoto(models.Model):
    MEDIA_TYPE_CHOICES = (
        ('photo', 'Photo'),
        ('video', 'Video'),
    )

    VISIBILITY_CHOICES = (
        ('A', 'Old Memory'),
        ('B', 'Student Events'),
        ('C', 'Our Picnic'),
        ('D', 'Recent'),
    )

    album = models.ForeignKey(
        AlumniAlbum, related_name='album', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    media_type = models.CharField(max_length=5, choices=MEDIA_TYPE_CHOICES)
    event_date = models.DateTimeField(auto_now=False)
    visibility_option = models.CharField(
        max_length=100, choices=VISIBILITY_CHOICES)
    photo = models.ImageField(
        upload_to='images/gallery/', blank=True, null=True)
    video_url = models.CharField(max_length=255, blank=True, null=True)
    is_published = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.media_type == 'photo' and not self.photo:
            raise ValidationError('Photo must have an image.')
        if self.media_type == 'video' and not self.video_url:
            raise ValidationError('Video must have a video url.')
        if self.media_type == 'photo' and self.video_url:
            raise ValidationError('Photo cannot have a video url.')
        # if self.media_type == 'video' and self.photo:
        #     raise ValidationError('Video cannot have an image.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def _str_(self):
        return f'{self.media_type} - {self.title}'


class Comment(models.Model):
    news = models.ForeignKey(
        NewsPost, on_delete=models.CASCADE, related_name='comment')
    author = models.ForeignKey(
        AlumniProfile, on_delete=models.CASCADE, related_name='author_comment')
    content = models.TextField()
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.author.user} on {self.news}'


class AlumniFAQ(models.Model):
    question = models.TextField()
    answer = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question[:50]

    class Meta:
        verbose_name = "Alumni FAQ"
        verbose_name_plural = "Alumni FAQs"
        ordering = ['-created_at']


class AlumniOfTheMonth(models.Model):
    # alumni_name = models.ForeignKey(
    #     AlumniProfile, on_delete=models.CASCADE, unique=True, related_name='alumni_name', null=False)
    alumni_name = models.OneToOneField(
        AlumniProfile, on_delete=models.CASCADE, related_name='alumni_name')
    descriptions = models.TextField(max_length=255, null=False)
    alumni_profile_picture = models.ImageField(
        upload_to='images/alumnimonth/', blank=True, null=True)
    is_active = models.BooleanField(default=False)
    optionone = models.TextField(max_length=255, null=True, blank=True)
    optiontwo = models.TextField(max_length=255, null=True, blank=True)
    optionthree = models.TextField(max_length=255, null=True, blank=True)
    optionfour = models.TextField(max_length=255, null=True, blank=True)
    optionfive = models.TextField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return f'{self.fullname.user.first_name.upper()} - {self.fullname.user.last_name.upper()}'

    def save(self, *args, **kwargs):
        if self.is_active:
            # Deactivate other entries
            AlumniOfTheMonth.objects.filter(
                is_active=True).update(is_active=False)
        super(AlumniOfTheMonth, self).save(*args, **kwargs)


class TrafficLog(models.Model):
    ip_address = models.GenericIPAddressField(null=True)
    user_agent = models.TextField(null=True)
    DEVICE_CHOICES = [
        ('desktop', 'Desktop'),
        ('mobile', 'Mobile'),
        ('tablet', 'Tablet'),
        ('other', 'Other'),
    ]

    timestamp = models.DateTimeField(auto_now_add=True)
    device_type = models.CharField(max_length=10, choices=DEVICE_CHOICES)
    last_activity = models.DateTimeField(auto_now=True)
