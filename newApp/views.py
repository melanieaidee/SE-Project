# Django core imports
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
# Forms
from .forms import UserUpdateForm, ProfileUpdateForm, PostForm
# Models
from .models import Follow, Post, Message, Notification
# Django REST Framework
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
# Serializers
from .serializers import NotificationSerializer
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
        #this will show message that it worked and then redirect to the login page
        messages.success(request, "Account created successfully")
        return redirect('login')
    #will render the signup page if the request method is not post
    return render(request, 'signup.html')
#####################################################################################################
#this is a signal that will create a profile for the user when they have registered
@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
#this is going to check if the request method is post then it will update the user and profile forms with the data from the request and save it

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
#this is the login view which will authenticate the user and log them in
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        #here is the authenticaton of the user with the given username and password 
        user = authenticate(
            request,
            username=username,
            password=password
        )
        #if the user is authenticated then log them in and redirect to the main home page
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
    return redirect("profile", username=username)
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
#this is to create a post that they can upload an image and write a caption that will later display on the main home page 
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  
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
        Notification.objects.create(
            recipient=post.user,
            message=f"{request.user.username} liked your post."
        )
    #will be on the profile as well as in the main_home
    return redirect(request.META.get('HTTP_REFERER', 'main_home'))
#####################################################################################################
#this is the user_list for that will show all the users except the curretn user 
@login_required
def users_list(request):
    users = User.objects.filter(is_superuser=False, is_staff=False).exclude(id=request.user.id)
    return render (request, "users_list.html", {"users": users})
#######################################################################################################
#this is the chat that will show the messages between the current user and the other user that they are messaging with and also check if 
#they are following each other or not so that if not it will show a message that they need to follow each other 
@login_required
def chat_view(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    if other_user == request.user:
        return redirect("main_home")

    follows_other = Follow.objects.filter(
        follower=request.user,
        following=other_user
    ).exists()

    other_follows = Follow.objects.filter(
        follower=other_user,
        following=request.user
    ).exists()

    is_mutual = follows_other and other_follows
    #this is going to get all the messages between the curretn user and the other user
    #with the order of the timestamp to show the messages in the order they were sent
    chat_messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by("timestamp")

    return render(request, "chat.html", {
        "other_user": other_user,
        "messages": chat_messages,
        "is_mutual": is_mutual,
        "follows_other": follows_other,
        "other_follows": other_follows,
    })
#########################################################################################################
#this is to send the message between the current user and the other user that they are messaging with and redirect them to the chat page after sending the message
@login_required
def send_message(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    if other_user == request.user:
        return redirect("main_home")

    follows_other = Follow.objects.filter(
        follower=request.user,
        following=other_user
    ).exists()

    other_follows = Follow.objects.filter(
        follower=other_user,
        following=request.user
    ).exists()

    if not (follows_other and other_follows):
        messages.error(
            request,
            "You must follow each other to send messages."
        )
        return redirect("chat", user_id=user_id)

    if request.method == "POST":
        body = request.POST.get("body", "").strip()

        if body:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                body=body
            )

    return redirect("chat", user_id=user_id)
#######################################################################################################
#this is the api view for teh notification list that will return the notifications
#for the current user in json format and also check if the user is authenticated or not to acess this api
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user
        ).order_by('-created_at')
#######################################################################################################
#this is for marking the notification as read when the user clicks on the notification and it will 
# update the is_read field to true and return a response that the notification has been marked as read 
# or if the notification is not found it will return a response that the notification is not found(got help from ai and other source)
# link: https://medium.com/@ytryqzdd/implementing-notifications-in-django-keep-your-users-informed-instantly-0523c1226900
class MarkNotificationReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk, recipient=request.user)
            notification.is_read = True
            notification.save()
            return Response({'status': 'notification marked as read'}, status=status.HTTP_200_OK)

        except Notification.DoesNotExist:
            return Response({'error': 'notification not found'}, status=status.HTTP_404_NOT_FOUND)
#######################################################################################################
#this is the view for the notifications page that will show the notificatons 
#for the curretn user in the html page and order them by the created_at field to show the most recent notifications 

def notifications_page(request):
    notifications = Notification.objects.filter(
        recipient=request.user
    ).order_by('-created_at')
    return render(request, "notifications.html", {"notifications": notifications})
#########################################################################################################
#this is the view for the profile page that will show updated edits

def edit_profile(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', request.user.username)
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})