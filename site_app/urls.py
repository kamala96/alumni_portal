from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('user_create_account', views.user_create_account,
         name='user_create_account'),
    path('user_create_login', views.login_view, name='user_create_login'),
    path('user_logout/', views.logout_view, name='user_logout'),
    path('usre_profile_image/', views.usre_profile_image,
         name='usre_profile_image'),
    path('alumni_update_password/', views.alumni_update_password,
         name='alumni_update_password'),
    path('alumni_update_profile/', views.alumni_update_profile,
         name='alumni_update_profile'),
    path('menu/<str:menu_slug>/', views.handle_nav_menu_click,
         name='handle_nav_menu_click'),
    path('default_error_page/', views.default_error_page,
         name='default_error_page'),
    path('event/<int:event_id>/', views.handle_event_click,
         name='handle_event_click'),
    path('news/<int:news_id>/', views.handle_news_click, name='handle_news_click'),
    path('gallery/<int:album_id>/', views.handle_album_click,
         name='handle_album_click'),
    path('user/<int:user_id>/', views.handle_user_profile_click,
         name='handle_user_profile_click'),
    path('add_subscribe/', views.add_subscribe, name='add_subscribe'),

]
