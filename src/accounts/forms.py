from django import forms
from django.forms import ModelForm

from .models import Accounts, Projects, Tasks_Projects

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
            'avatar': forms.FileInput(attrs={'accept': 'image/', 'class': 'form-control-file'}),
            'password': forms.TextInput(attrs={'type': 'password', 'class': 'form-control-file', 'placeholder': 'Змінити пароль'})
        }


class CreateProjects(forms.ModelForm):
    class Meta:
   
        model = Projects
        fields = ['title', 'start_date', 'end_date', 'team_members', 'access']

        labels = {
            'title': "Назва проекту",
            'start_date': 'Початок проекту',
            'end_date': 'Закінчення проекту',
            'team_members': 'Учасники',
            'access': 'Хто має доступ керування проектом'
        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ведіть назву проекту"}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}),
            'team_members': forms.Select(attrs={'class': 'form-control'}, choices=[('Я', 'Я')]),
            'access': forms.Select(attrs={'class': 'form-control'}, choices=[('Я', 'Я')]),
        }


class TaskProjects(forms.ModelForm):
    class Meta:
        model = Tasks_Projects
        fields = "__all__"

        labels = {
            'title': "Назва задачи",
            'description': 'Опис задачи',
            'perform': "Хто виконує (по стандарту 'всі')",
            'end_date': 'Коли закінчити задачу'
        }