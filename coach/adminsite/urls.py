"""adminsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from adminpanel import views
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView


urlpatterns = [
    # path('', views.home, name='home'),
    path('', admin.site.urls),
    # path('users/', views.user_list, name='user_list'),

    # # path('users_list/', views.users_list, name='users_list'),
    # path('files/<int:file_id>/edit-file/', views.edit_file, name='edit_file'),

    # path('files/', views.file_list, name='file_list'),
    # path('delete_file/<int:file_id>/', views.delete_file, name='delete_file'),
    # # path('files/<int:file_id>/edit-file/', views.edit_file, name='edit_file'),


    # path('subscriptions/', views.subscriptions_list, name='subscriptions_list'),
    # path('login/', views.CustomLoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

    # # path('users/', views.user_list, name='user_list'),
    # path('users/<int:user_id>/edit-username/',
    #      views.edit_username, name='edit_username'),
    # path('users/new/', 
    #      views.new_user, name='new_user'),
    # path('users/<int:user_id>/edit-subscriptions/',
    #      views.edit_subscriptions, name='edit_subscriptions'),
    # path('delete_user/<int:user_id>/', 
    #      views.delete_user, name='delete_user'),
    # path('user/subscriptions/<int:user_id>/',
    #      views.user_subscriptions, name='user_subscriptions'),


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
