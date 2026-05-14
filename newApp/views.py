# Django core imports
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
# Forms
from .forms import UserUpdateForm, ProfileUpdateForm, PostForm
# Models
from .models import Follow, Post, Message, Notification, Comment
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
    posts = Post.objects.all().order_by('-created_at').prefetch_related('comments')
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
# Handles the creation of a new post by the logged‑in user
@login_required
def create_post(request):
    # If the form was submitted, process the POST data
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        # Validate the form before saving
        if form.is_valid():
            # Create the post object but don't save it yet
            post = form.save(commit=False)
            # Assign the current user as the post owner
            post.user = request.user
            # Save the completed post to the database
            post.save()
            # Redirect to the home page after successful creation
            return redirect('main_home')
    else:
        # If it's a GET request, display an empty form
        form = PostForm()
    # Render the post creation page with the form
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
# Redirects the logged in user to their own profile pag
@login_required
def my_profile_redirect(request):
    # Send the user to their profile using their username in the URL
    return redirect('profile', username=request.user.username)
#####################################################################################################
def like_post(request, post_id):
    # Get the user you are trying to like or unlike, or return 404 if not found
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
    # Get all non-admin users (no superusers, no staff accounts)
    # Exclude the current user so they don't see themselves in the list
    users = User.objects.filter(is_superuser=False, is_staff=False).exclude(id=request.user.id)
    return render (request, "users_list.html", {"users": users})
#######################################################################################################
#this is the chat that will show the messages between the current user and the other user that they are messaging with and also check if 
#they are following each other or not so that if not it will show a message that they need to follow each other 
@login_required
def chat_view(request, user_id):
    # Get the user you are trying to chat with (or return 404 if not found)
    other_user = get_object_or_404(User, id=user_id)
    # Prevent users from opening a chat with themselves
    if other_user == request.user:
        return redirect("main_home")
    #checks for mutual following
    follows_other = Follow.objects.filter(
        follower=request.user,
        following=other_user
    ).exists()
    # Does the other user follow the current user?
    other_follows = Follow.objects.filter(
        follower=other_user,
        following=request.user
    ).exists()
    # Only allow chat if both follow each other
    can_chat = follows_other and other_follows
    # Get messages b/t to users
    # This retrieves every message where:
    # sender is either user
    # receiver is either user
    # Then orders them by timestamp (oldest → newest)
    chat_messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by("timestamp")
    # other_user, who you're chatting with
    # messages , the conversation history
    # can_chat , whether mutual follow exists
    return render(request, "chat.html", {
        "other_user": other_user,
        "messages": chat_messages,
        "can_chat": can_chat,
    })
#########################################################################################################
#this is to send the message between the current user and the other user that they are messaging with and redirect them to the chat page after sending the message
@login_required
def send_message(request, user_id):
    # Get the user you are trying to message, or return 404 if not found
    other_user = get_object_or_404(User, id=user_id)
    #Prevent users from messaging themselves
    if other_user == request.user:
        return redirect("main_home")
    #check if you follow the other user
    follows_other = Follow.objects.filter(
        follower=request.user,
        following=other_user
    ).exists()
    #check if other user follows you
    other_follows = Follow.objects.filter(
        follower=other_user,
        following=request.user
    ).exists()
    #handle message submission
    if request.method == "POST":
        #Get the message text and remove extra spaces
        body = request.POST.get("body", "").strip()
        #only create a messafe if the body is not empty
        if body:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                body=body
            )
    #redirect back to the chat page
    return redirect("chat", user_id=user_id)
#######################################################################################################
# API view returns all notifications for the authenticated user in JSON format.
# This endpoint is used by the frontend (JavaScript) to fetch the user's notifications
# without reloading the page. It allows your app to:
# Display notifications dynamically in the navbar
# Poll for new notifications every few seconds 
# Update the UI in real time when new notifications arrive
# Keep unread/read status synced between backend and frontend
# The view ensures that only the logged‑in user's notifications are returned, they are ordered from newest to oldest
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only return notifications that belong to the current user,
        # ordered by newest first.
        return Notification.objects.filter(
            recipient=self.request.user
        ).order_by('-created_at')

#######################################################################################################
# link: https://medium.com/@ytryqzdd/implementing-notifications-in-django-keep-your-users-informed-instantly-0523c1226900
# API view marks a specific notification as read. This endpoint is called when the
# frontend sends a POST request after the user clicks a notification. The view checks
# that the notification exists and belongs to the authenticated user, then updates the
# is_read field to True in the database. If the notification is found and updated,
# the API returns a success response. If the notification does not exist or does not
# belong to the current user, the API returns an error response. This keeps the read
# status in sync between the backend and the frontend and ensures users cannot access
# or modify notifications that are not theirs.
class MarkNotificationReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk):
        # Try to find the notification that belongs to the current user.
        try:
            notification = Notification.objects.get(pk=pk, recipient=request.user)
            notification.is_read = True
            notification.save()
            return Response(
                {'status': 'notification marked as read'},
                status=status.HTTP_200_OK
            )
        # If the notification doesn't exist or doesn't belong to the user.
        except Notification.DoesNotExist:
            return Response(
                {'error': 'notification not found'},
                status=status.HTTP_404_NOT_FOUND
            )
#######################################################################################################
# HTML view displays the notifications page for the logged‑in user. This view retrieves
# all unread notifications that belong to the current user and sends them to the
# notifications.html template. The notifications are ordered from newest to oldest so
# the most recent activity appears first. This view is used when the user navigates to
# the notifications page in the browser, and it renders the page normally rather than
# returning JSON. It ensures that only the authenticated user's notifications are shown
# and keeps the unread list accurate on the frontend.
@login_required
def notifications_page(request):
    notifications = Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).order_by('-created_at')

    return render(request, 'notifications.html', {
        'notifications': notifications
    })
#######################################################################################################
# HTML view marks a notification as read when the user clicks it. This view is used
# when the user interacts with a notification through the regular website rather than
# through an API call. It verifies that the notification exists and belongs to the
# currently authenticated user to prevent anyone from accessing or modifying another
# user's notifications. Once the notification is confirmed, it updates the is_read
# field to True and saves the change. After updating the notification, the user is
# redirected back to the notifications page so the interface immediately reflects the
# updated read status.
# Marks a specific notification as read when the user clicks it
@login_required
def mark_notification_read(request, pk):
    # Ensure the notification exists and belongs to the current user.
    # get_object_or_404 prevents unauthorized access to another user's notifications.
    notif = get_object_or_404(Notification, pk=pk, recipient=request.user)
    # Update the notification's read status
    notif.is_read = True
    notif.save()
    # Redirect back to the notifications page so the UI updates immediately
    return redirect('notifications-page')
###########################################################################################
#this is the view for adding a  comment to a post and creating a notification for the 
# post owner when someone comments on their post and then redirecting to the main home page after adding the comment
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    text = request.POST.get("text")

    Comment.objects.create(
        user=request.user,
        post=post,
        text=text
    )

    # Create notification
    if request.user != post.user:
        Notification.objects.create(
            recipient=post.user,
            message=f"{request.user.username} commented on your post."
        )
    #redirects back to comment page
    return redirect('comments_page', post_id=post.id)
###########################################################################################
@login_required
def comments_page(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()

    return render(request, 'comments_page.html', {
        'post': post,
        'comments': comments
    })
###########################################################################################
#this is the view for sharing a post to another user through the chat by sending a message with the link to the post 
# and the username of the user who shared it and then redirecting to the chat page with that user
@login_required
def share_post_to_user(request, post_id, receiver_id):
    post = get_object_or_404(Post, id=post_id)
    receiver = get_object_or_404(User, id=receiver_id)

    Message.objects.create(
        sender=request.user,
        receiver=receiver,
        body=f"{request.user.username} shared a post with you: http://127.0.0.1:8000/main_home/#post-{post.id}")
    return redirect("chat", user_id=receiver.id)
###########################################################################################
# this is the view for searching users based on campus selection and name/username input
# it allows the user to pick a campus (Edinburg or Brownsville) and then type a name
# the view filters the User model by the selected campus and the search text
# and returns a list of matching users so the user can view their profile or message them
def user_search(request):
    query = request.GET.get("q", "")          # the text the user typed in the search bar
    campus = request.GET.get("campus", "")    # the campus selected from the dropdown

    users = User.objects.all()                # start with all users

    # EXCLUDE ADMIN so that it doesn't show in the search
    users = users.exclude(is_superuser=True).exclude(is_staff=True)

    # filter by campus if the user selected one
    if campus:
        users = users.filter(profile__enrolled=campus)

    # filter by search text (username OR first name OR last name)
    if query:
        users_username = users.filter(username__icontains=query)
        users_first = users.filter(first_name__icontains=query)
        users_last = users.filter(last_name__icontains=query)

        # combine all results and remove duplicates
        users = (users_username | users_first | users_last).distinct()

    # return the filtered users to the template
    return render(request, "user_search.html", {
        "query": query,
        "campus": campus,
        "users": users,
    })
