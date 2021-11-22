from django import forms
from django.forms import ModelForm, fields
from .models import Profile

class ProfileForm(ModelForm):
    class Meta:
        model=Profile
        fields={'profile_pic'}

