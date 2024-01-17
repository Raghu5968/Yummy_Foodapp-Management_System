from django import forms
from .models import *
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

class foodappform(forms.ModelForm):
    class Meta:
        model=Foodappusers
        fields="__all__"
        exclude=['user']

class itemform(forms.ModelForm):
    class Meta:
        model=Item
        fields="__all__"

class Orderform(forms.ModelForm):
    class Meta:
        model=Order
        fields="__all__"
        exclude=['status']


class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']

class feedbackform(forms.ModelForm):
    class Meta:
        model=feedback
        fields="__all__"

class slrform(forms.ModelForm):
    class Meta:
        model=Seller
        fields="__all__"