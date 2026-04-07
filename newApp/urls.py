from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.home, name = 'home'),
    path('register/', views.register, name = 'register'),
    path('profile/', views.profile, name = 'profile'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name = 'login'),
    path('logout/', views.logout_view, name='logout'),#redirect to home after logout
    path('main_home/', views.main_home, name='main_home'), #created this  
    path("follow/<str:username>/", views.follow_view, name="follow_view"),#this is the follow view with the username
    path("user/<str:username>/", views.user_profile, name="user_profile"),#this is the user profile view with the username
]
