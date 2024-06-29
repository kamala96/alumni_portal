from django.contrib import admin

from .models import * #TopHeader, Navigationmenu, ASiteSettings, EventsPost, NewsPost, JobPosting



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


@admin.register(EventsPost)
class EventsPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at')
    # list_filter = ('is_active', 'created_at', 'updated_at')
    # search_fields = ('main_logo', 'favourite_icon')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at')
    # list_filter = ('is_active', 'created_at', 'updated_at')
    # search_fields = ('main_logo', 'favourite_icon')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'updated_at')

@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')

@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')

@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')

@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_slider_active', 'created_at', 'updated_at')
    prepopulated_fields = {"slug": ("title",)}

@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'link_type', 'url', 'is_active', 'is_for_newtab', 'created', 'updated')
    list_filter = ('link_type', 'is_active', 'created', 'updated')
    search_fields = ('name', 'url')
@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('email',)



@admin.register(Responsibility)
class ResponsibilityAdmin(admin.ModelAdmin):
    list_display = ('title', 'desc', 'image', 'created')
    # prepopulated_fields = {"slug": ("title",)}
