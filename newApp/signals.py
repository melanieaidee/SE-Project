from django.contrib.auth.models import User 
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
#this below is a decorator for a specific condition, not an if statement.
@receiver(post_save, sender = User)
#create an intance for every users to signal that they created their account
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)
        
        
