#add the forms for our models

from django import forms
from django.contrib.auth.models import User
from .models import Profile
from .models import Post
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
        fields = ['bio', 'enrolled']
#creating a post
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [ 'content', 'image']#this is for the styling of the form
        #this is the widgets for the form to make it look better
        widgets = {
                'content': forms.Textarea(attrs={'class': 'form-control'}),
                'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            }
    #this is a function that for the description of the post will have at least 300 words
    def clean_content(self):
        content = self.cleaned_data.get('content')
        word_count = len(content.split())

        if word_count > 300:
            raise forms.ValidationError("Cannot exceed 300 words.")

        return content
    