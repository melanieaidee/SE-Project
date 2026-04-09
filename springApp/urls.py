
from django.contrib import admin
from django.urls import path, include 
from newApp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('newApp.urls')),
    path('signup/', views.signup, name = 'signup')
]
