from django import forms
from django.contrib.auth.models import  User
from app_admin.models import UserProfileInfo

class FormUser(forms.ModelForm):
    username = forms.CharField(label='Username',  widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    email = forms.CharField(label='Email',  widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))
    password = forms.CharField(label='Password',  widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))
    confirm_password = forms.CharField(label='Confirm Password',  widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))
    first_name = forms.CharField(label='First name',  widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    last_name = forms.CharField(label='Last name',  widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

class FormUserProfileInfo(forms.ModelForm):
    porfolio = forms.URLField(label ='Porfolio', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    image = forms.ImageField(label ='Image', required=False, widget=forms.FileInput(attrs={
        'class': 'form-control-file'
    }))

    class Meta:
        model = UserProfileInfo
        exclude = ['user']