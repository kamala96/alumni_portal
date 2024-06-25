from django.contrib import admin
from .models import TopHeader, Navigationmenu, ASiteSettings

# Register your models here.
@admin.register(TopHeader)
class TopHeaderAdmin(admin.ModelAdmin):
    list_display = ('MenuFor','title', 'position', 'link_type', 'link', 'icon_class', 'is_active')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Navigationmenu)
class NavigationmenuAdmin(admin.ModelAdmin):
    list_display = ('menu_name', 'menu_type', 'indentation', 'parent', 'order_id', 'is_active')
    list_filter = ('menu_type', 'is_active')
    search_fields = ('menu_name',)
    prepopulated_fields = {'slug': ('menu_name',)}

@admin.register(ASiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'main_logo', 'favourite_icon', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('main_logo', 'favourite_icon')