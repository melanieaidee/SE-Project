from django.db import models
from django.contrib.auth.models import User 
#what is a user for jango we can do our own models
# Create your models here.
#we can add as many as we want
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
    