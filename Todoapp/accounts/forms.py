from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

class RegisterForm(UserCreationForm):
  email = forms.EmailField(required=True)

  class Meta:
    model = get_user_model()
    fields = ['first_name', 'last_name', 'email','password1','password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username')