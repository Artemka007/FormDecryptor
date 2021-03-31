from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='Email address: ', required=True, max_length=100)
    first_name = forms.EmailField(label='First name: ', required=True, max_length=100)
    last_name = forms.EmailField(label='Last name: ', required=True, max_length=100)
    class Meta:
        model = User
        # Здесь к стандартной форме, от которой наследуется эта форма добавляем имя и фамилию пользователя
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']