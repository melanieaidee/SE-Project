#add the forms for our models

from django import forms
from django.contrib.auth.models import User
from .models import Profile
#both classes are different not the same!!
#updating the user
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name', 'email']

#updating the profile
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio','student_id', 'enrolled']