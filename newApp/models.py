from django.db import models
from django.contrib.auth.models import User 
#we can create models like spotify for example, you need the name of the song
#lyrics, lenght of the song, album....
#just like our user is our model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    student_id = models.IntegerField(blank=True, null=True)
    enrolled = models.BooleanField(default=False)

    
    def __str__(self):
        return self.user.username
#this is the follow model which will be used to create the follow and unfollow functionality

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
