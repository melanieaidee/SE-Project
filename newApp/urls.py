from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import (
    NotificationListView,
    MarkNotificationReadView,
    notifications_page,   
)
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.my_profile_redirect, name='my_profile'),
    path("profile/<str:username>/", views.profile_view, name="profile"),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('main_home/', views.main_home, name='main_home'),

    # FOLLOW SYSTEM
    path("follow/<str:username>/", views.follow_view, name="follow_view"),
    path("<str:username>/followers/", views.followers_lists, name="followers_lists"),
    path("<str:username>/following/", views.following_lists, name="following_lists"),

    # POSTS
    path('create/', views.create_post, name='create_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),

    # COMMENTS
    path("comment/<int:post_id>/", views.add_comment, name="add_comment"),
    path("post/<int:post_id>/comments/", views.comments_page, name="comments_page"),  # ⭐ ADDED

    # MESSAGING
    path("inbox/", views.users_list, name="users_list"),
    path("chat/<int:user_id>/", views.chat_view, name="chat"),
    path("send/<int:user_id>/", views.send_message, name="send_message"),

    # SHARE POST
    path("share/<int:post_id>/<int:receiver_id>/", views.share_post_to_user, name="share-post"),

    # NOTIFICATIONS
    path('notifications/', NotificationListView.as_view(), name='notifications-list'),
    path("notifications-page/", notifications_page, name="notifications-page"),
    path('notifications/<int:pk>/read/', views.mark_notification_read, name='mark-notification-read'),

    #SEARCH
    path("search/", views.user_search, name="user_search"),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
