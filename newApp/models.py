from django.db import models
from django.contrib.auth.models import User 
#we can create models like spotify for example, you need the name of the song
#lyrics, lenght of the song, album....
#just like our user is our model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
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
    def __str__(self):
        return self.titl