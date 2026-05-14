from django.db import models
from django.contrib.auth.models import User 

#we can create models like spotify for example, you need the name of the song
#lyrics, lenght of the song, album....
#just like our user is our model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    ENROLLED_CHOICES = [
        ('ED', 'Edinburg'),
        ('BR', 'Brownsville'),
        
    ]
    enrolled = models.CharField(
        max_length=20,
        choices=ENROLLED_CHOICES,
        default='ED'
    )
    def __str__(self):
        return self.user.username
#this is the follow model which will be used to create the follow and unfollow functionality

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

class Post(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='blogpost_like', blank=True)
   
    def likes_count(self):
        return self.likes.count()
    
    #return the number of likes for a post
    def __str__(self):
        return f"{self.user.username}'s post at {self.created_at}"
    #this will be the function delete post that will remove the post and image from the database
    def delete(self,*arg,**kwargs):
        #deletes the image file from the vs storage when the post is deleted
        if self.image:
            self.image.delete(save=False)
        super().delete(*arg,**kwargs)
#this is the message model for the functuonality of sending message only between users no group chat
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender} → {self.receiver}: {self.body[:20]}"
#api for notifications
class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.message[:20]}"
#this will be the comment model 
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} commented on {self.post.id}: {self.text[:20]}"