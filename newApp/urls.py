from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from newApp import views
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('main_home/', views.main_home, name='main_home'),
    path("follow/<str:username>/", views.follow_view, name="follow_view"),
    path("user/<str:username>/", views.user_profile, name="user_profile"),
    path("<str:username>/followers/", views.followers_lists, name="followers_lists"),
    path("<str:username>/following/", views.following_lists, name="following_lists"),
]


