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
from .forms import PostForm #added this for the post form
from .models import Post #added this for the post model
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import redirect

#####################################################################################################
#this is the home view which will be the page before login
def home(request):
    return render(request, 'home.html', {})
#####################################################################################################
#added main_home view this will be the main page after login 
def main_home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'main_home.html', {'posts': posts})
#####################################################################################################
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # if Passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        # Must be a UTRGV email
        if not email.endswith("@utrgv.edu"):
            messages.error(request, "Email must be a UTRGV email")
            return redirect('register')

        # warned about username taken
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('register')

        # warned about email already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('register')

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'signup.html')
#####################################################################################################
#this is a signal that will create a profile for the user when they have registered
@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
#this is going to check if the request method is post then it will update the user and profile forms with the data from the request and save it
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your changes have been saved!")
            return redirect('profile', username=request.user.username)
    else:
        u_form = UserUpdateForm(instance=profile_user)
        p_form = ProfileUpdateForm(instance=profile_user.profile)
#this is going to get all the posts for the user and order them by the created_at field
    posts = Post.objects.filter(user=profile_user).order_by('-created_at')
    posts_count = posts.count()
#this is going to get the number of followers/following for the user and check if the current user is followirng or not
    followers_count = Follow.objects.filter(following=profile_user).count()
    following_count = Follow.objects.filter(follower=profile_user).count()

    is_following = Follow.objects.filter(
        follower=request.user,
        following=profile_user
    ).exists()

    return render(request, 'profile.html', {
        'profile_user': profile_user,
        'posts': posts,
        'posts_count': posts_count,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
        'u_form': u_form,
        'p_form': p_form,
    })

#####################################################################################################
@login_required
def my_profile_redirect(request):
    return redirect('profile', username=request.user.username)

#####################################################################################################
#this is the login view which will authenticate the user and log them in
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        #this is going to the authenticate func to check if the username and password are correct
        user = authenticate(request, username=username, password=password)
    #if the user is autheticated then the log in will direct them to the main home page else it wont unless they enter the correct username and password
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
#will separate the followers and following lists into their own views and templates easier not to mess it up
#this will be the followers view for the user to direct them to the followers list of users   

def followers_lists(request, username):
    list_users = get_object_or_404(User, username=username)#this is the user whose followers we want to see
    followers = list_users.followers.all()
    return render(request, 'followers_lists.html', {
        'list_users': list_users,
        'followers': followers,
        
    })
#####################################################################################################
#this will be the following view for the user to direct them to the following list of users   
def following_lists(request, username):
    list_users = get_object_or_404(User, username=username)#this is the user whose followers we want to see
    following = list_users.following.all()
    return render(request, 'following_lists.html', {
        'list_users': list_users,
        'following': following,
        
    })
#####################################################################################################

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user   # ← attach the user
            post.save()
            return redirect('main_home')
    else:
        form = PostForm()

    return render(request, 'create_post.html', {'form': form})
#####################################################################################################
def delete_post(request, *args, **kwargs):
    post_id = kwargs.get('post_id')#this is going to get the post_id from the url and use it to get the post object that we want to delete
    post = get_object_or_404(Post, id=post_id)#this is going to get the post object with the given post_id/return a 404 error if it doesn't exist

    # Only allow the owner of the post to delete
    if request.user == post.user:
        post.delete()

    #this will redirect to the profile page after d;eting the post
    return redirect('profile', username=request.user.username)
#####################################################################################################
@login_required
def my_profile_redirect(request):
    return redirect('profile', username=request.user.username)
#####################################################################################################
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)  # Unlike the post
    else:
        post.likes.add(request.user)  # Like the post
    #will be on the profile as well as in the main_home
    return redirect(request.META.get('HTTP_REFERER', 'main_home'))