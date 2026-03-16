from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm
from django.forms.widgets import FileInput
from django.contrib.auth import models as auth_models
from user import models as user_models


class RegisterForm(UserCreationForm):
    class Meta:
        model = auth_models.User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {
            'username': 'Your username has a maxium of 150 characters and contains letters, digits and @ . + - _ only.'
        }


class LoginForm(AuthenticationForm):
    pass


class UserUpdateForm(ModelForm):
    class Meta:
        model = auth_models.User
        fields = ['username', 'email']
        help_texts = {
            'username': 'Your username has a maxium of 150 characters and contains letters, digits and @ . + - _ only.'
        }


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = user_models.Profile
        fields = ['biography', 'image']
        widgets = {
            'image': FileInput
        }