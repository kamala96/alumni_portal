from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import * #TopHeader, Navigationmenu, ASiteSettings, EventsPost, NewsPost, JobPosting



class AlumniProfileInline(admin.StackedInline):
    model = AlumniProfile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (AlumniProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)



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



@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('welcome_note', 'is_active', 'created_at')
    # prepopulated_fields = {"slug": ("title",)}


@admin.register(AlumniCommittee)
class AlumniCommitteeAdmin(admin.ModelAdmin):
    list_display = ('alumni_position', 'is_active', 'created_at')
    


@admin.register(AlumniSpeech)
class AlumniSpeechAdmin(admin.ModelAdmin):
    list_display = ('speech', 'is_published', 'created_at')


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ('name','text_to_display','url')



class AlbumPhotoInline(admin.TabularInline):
    model = AlbumPhoto
    extra = 1

@admin.register(AlumniAlbum)
class AlumniAlbumAdmin(admin.ModelAdmin):
    inlines = [AlbumPhotoInline]
    list_display = ('title', 'description', 'created_at')


@admin.register(AlumniFAQ)
class AlumniFAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('question', 'answer')
    readonly_fields = ('created_at', 'updated_at')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.order_by('-created_at')

    fieldsets = (
        (None, {
            'fields': ('question', 'answer', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


@admin.register(AlumniOfTheMonth)
class AlumniOfTheMonthAdmin(admin.ModelAdmin):
    list_display = ('alumni_name', 'descriptions', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('alumni_name__user__first_name', 'alumni_name__user__last_name')

    def save_model(self, request, obj, form, change):
        if obj.is_active:
            AlumniOfTheMonth.objects.filter(is_active=True).update(is_active=False)
        super().save_model(request, obj, form, change)

