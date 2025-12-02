from django import forms
from django.contrib.auth.models import User
from item.models import Item

class RegistrationForm(forms.ModelForm): 

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:

        model = User

        fields = ['username', 'email', 'password']


class LoginForm(forms.Form):

    username = forms.CharField()

    password = forms.CharField()


class ItemForm(forms.ModelForm):

    class Meta:

        model = Item

        fields = ['title', 'description']
