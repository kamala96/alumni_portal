from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.db import models

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
    MENU_TYPE_CHOICES = [
        ('main', 'Main'),
        ('sub', 'Sub'),
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
        limit_choices_to={'menu_type': 'main'}
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
    main_logo = models.ImageField(upload_to='static/images/logo/', blank=True, null=True)
    favourite_icon = models.ImageField(upload_to='static/images/favicon/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Site Setting"
