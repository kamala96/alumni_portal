from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('menu/<str:menu_slug>/', views.handle_nav_menu_click, name='handle_nav_menu_click'),
    path('default_error_page/', views.default_error_page, name='default_error_page'),
]
