from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from newApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.my_profile_redirect, name='my_profile'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('main_home/', views.main_home, name='main_home'),
    path("follow/<str:username>/", views.follow_view, name="follow_view"),
    path("<str:username>/followers/", views.followers_lists, name="followers_lists"),
    path("<str:username>/following/", views.following_lists, name="following_lists"),
    path('create/', views.create_post, name='create_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
]

#this is for the media files to be served during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



