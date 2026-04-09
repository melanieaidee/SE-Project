from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from newApp import views
urlpatterns = [
    path('', views.home, name = 'home'),
    path('register/', views.register, name = 'register'),
    path('profile/', views.profile, name = 'profile'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name = 'login'),
    path('signup/', views.signup, name = 'signup'),
    path('logout/', views.logout_view, name='logout'),#redirect to home after logout
    path('main_home/', views.main_home, name='main_home') #created this 
   
]
