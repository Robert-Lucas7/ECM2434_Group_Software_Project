# Code by Henry

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
        fields = ['username', 'email', 'password1', 'password2', 'profile_picture']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@exeter.ac.uk'):
            raise forms.ValidationError('You must have an exeter univerity email to register')
        return email


class MakePost(forms.Form):
    comment = forms.CharField(
        max_length=200, 
        widget=forms.Textarea(attrs={'style': 'width: 300px; height: 100px;'})
    )


class ChangeProfilePicture(forms.Form):
    profile_picture = forms.CharField(max_length=25)
