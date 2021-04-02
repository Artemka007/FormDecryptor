from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import gettext_lazy as _


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='Email address ', required=True, max_length=100)
    first_name = forms.CharField(label='First name ', required=True, max_length=100)
    last_name = forms.CharField(label='Last name ', required=True, max_length=100)
    class Meta:
        model = User
        # Здесь к стандартной форме, от которой наследуется эта форма добавляем имя и фамилию пользователя
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class EditUserForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        error_messages={
            'unique': _("A user with that username already exists."),
        },
        widget=forms.TextInput(attrs={'placeholder': 'Логин...'}),
        label=''
    )
    first_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'placeholder': 'Имя...'}), label='')
    last_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'placeholder': 'Фамилия...'}), label='')
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email...'}), label='')
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
