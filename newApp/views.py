from urllib import request

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login # will be exclusive 
from django.contrib.auth import logout

from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from .models import Follow 
#####################################################################################################
#this is the home view which will be the page before login
def home(request):
    return render(request, 'home.html', {})
#####################################################################################################
#added main_home view this will be the main page after login 
def main_home(request):
    return render(request, 'main_home.html', {})
#####################################################################################################
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully")
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})
#####################################################################################################
@login_required
def profile(request):
    profile_user = request.user  # the user whose profile is being viewed
    followers_count = profile_user.followers.count()
    following_count = profile_user.following.count()
    #if the request method is POST, we will update the user's information
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your account has been updated successfully")
            return redirect('profile')
    #if the request method is not POST, we will create the forms with the current user's information
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    # they cannot follow themselves, so always false
    return render(request, 'profile.html', {
        'u_form': u_form,#this is for the user update form
        'p_form': p_form,#this is for the profile update form
        'profile_user': profile_user,#this is for the profile user
        'followers_count': followers_count,#this is for the followers count
        'following_count': following_count,#this is fo rthe following count
        'is_following': False,#user cannot follow themselves so always false
    })

#####################################################################################################
#added this 
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('main_home') 
    return render(request, 'login.html')

#####################################################################################################
#this is the logout view which will log the user out and redirect to home page
def logout_view(request):
    logout(request)
    return redirect('home')
#####################################################################################################
#this will be the profile view with the username
def follow_view(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    current_user = request.user
#checks if the user is already following the user they want to follow
    existing_account = Follow.objects.filter(
        follower=current_user,
        following=user_to_follow
    )
#if statement to check if user is already following else create a new follow object
    if existing_account.exists():
        existing_account.delete()
    else:
        Follow.objects.create(
            follower=current_user,#this is the current user who is following
            following=user_to_follow #this is the user they want to follow
        )
#redirect to the profile page
    return redirect("user_profile", username=username)

#####################################################################################################
#this is the user profile view which will show the user's profile and the follow button
def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)

    is_following = Follow.objects.filter(
        follower=request.user,
        following=profile_user
    ).exists()

    followers_count = profile_user.followers.count()
    following_count = profile_user.following.count()

    return render(request, 'profile.html', {
        'profile_user': profile_user,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
    })
