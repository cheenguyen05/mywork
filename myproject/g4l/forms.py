
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django.forms.widgets import PasswordInput, TextInput, NumberInput

from django import forms
 
from .models import Profile


# - Create/Register a user (Model Form)

class CreateUserForm(UserCreationForm):
    school = forms.CharField(required=False)
    age = forms.IntegerField(required=False)

    class Meta:

        model = User
        fields = ['username', 'email', 'password1', 'password2']


    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            profile = Profile(user=user, school=self.cleaned_data['school'], age=self.cleaned_data['age'])
            profile.save()
        return user


# - Authenticate a user (Model Form)

class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email'] 

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['school', 'age']

