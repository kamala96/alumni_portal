from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.db import models

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
