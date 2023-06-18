from django import forms
from django.forms import ModelForm

from .models import Accounts

# create account form, sign up
class AccountsForm_SignUp(ModelForm):
    class Meta:
        model = Accounts
        fields = "__all__"

        labels = {
            'name': "Ваше ім'я",
            'login': 'Ведіть логін, по ньому вас зможуть знайти у мережі',
            'email': 'Ведіть вашу пошту',
            'password': 'Ведіть надійний пароль'
        }
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ведіть ваше ім'я"}),
            'login': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ведіть логін'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ведіть пошту'}),
            'avatar': forms.FileInput(attrs={'type': 'file', 'accept': 'image/', 'class': 'form-control-file'}),
            'password': forms.TextInput(attrs={'type': 'password', 'class': 'form-control-file', 'placeholder': 'Ведіть пароль'})
        }


class AccountsForm_SignIn(ModelForm):
    class Meta:
        model = Accounts
        fields = ('login', 'password')

        labels = {
            'login': 'Ведіть логін',
            'password': 'Ведіть ваш пароль'
        }
        
        widgets = {
            'login': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ведіть логін'}),
            'password': forms.TextInput(attrs={'type': 'password', 'class': 'form-control-file', 'placeholder': 'Ведіть пароль'})
        }


class UpdateAccount(forms.ModelForm):
    class Meta:
        model = Accounts
        fields = "__all__"

        labels = {
            'name': "Змінити ім'я",
            'login': 'Змінити логін',
            'email': 'Змінити пошту',
            'password': 'Змінити пароль'
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Змінити ім'я"}),
            'login': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Змінити логін'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Змінити пошту'}),
            'avatar': forms.FileInput(attrs={'type': 'file', 'accept': 'image/', 'class': 'form-control-file'}),
            'password': forms.TextInput(attrs={'type': 'password', 'class': 'form-control-file', 'placeholder': 'Змінити пароль'})
        }