from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',  # Optional: Customize the placeholder text
        })
    )


class Signup(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
