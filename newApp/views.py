from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login # will be exclusive 
from django.contrib.auth import logout

#this is the home view which will be the page before login
def home(request):
    return render(request, 'home.html', {})
#added main_home view this will be the main page after login 
def main_home(request):
    return render(request, 'main_home.html', {})

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


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your account has been updated successfully")
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'profile.html', {'u_form': u_form, 'p_form': p_form})
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
#this is the logout view which will log the user out and redirect to home page
def logout_view(request):
    logout(request)
    return redirect('home')

def signup(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')