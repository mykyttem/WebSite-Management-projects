from django import forms
from .models import Projects, Tasks_Projects, MembersProject

class CreateProjects(forms.ModelForm):
    class Meta:
   
        model = Projects
        fields = ['title', 'deadline', 'access']

        labels = {
            'title': "Назва проекту",
            'access': 'Хто має доступ керування проектом',
            'deadline': 'Крайний термін'
        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ведіть назву проекту"}),
            'deadline': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}),
            'access': forms.Select(attrs={'class': 'form-control'}, choices=[('Я', 'Я')]),
        }


class SettingsProject(forms.ModelForm):
    # get the current value
    def __init__(self, info_project, *args, **kwargs):
        super(SettingsProject, self).__init__(*args, **kwargs)
        self.info_project = info_project
        
        for i in self.info_project:
            
            # set value for fields
            self.fields['title'].widget.attrs['value'] = i['title']

            if isinstance(self.fields['status'].widget, forms.Select):
                self.fields['status'].initial = i['status']


    class Meta:
        model = Projects
        fields = ['title', 'deadline', 'access', 'status']

        labels = {
            'title': "Назва проекту",
            'status': 'Статус',
            'access': 'Хто має доступ керування проектом',
            'deadline': 'Крайний термін'
        }
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Змінити назву проекту"}),
            'deadline': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}, choices=[('В розробці', 'В розробці'), ('Завершено', 'Завершено')]),
            'access': forms.Select(attrs={'class': 'form-control'}, choices=[('Я', 'Я')])
        }


class TaskProjects(forms.ModelForm):
    class Meta:
        model = Tasks_Projects
        fields = ['title', 'description', 'perform', 'end_date', 'status']

        labels = {
            'title': "Назва задачи",
            'description': 'Опис задачи',
            'perform': "Хто виконує (по стандарту 'всі')",
            'status': 'Статус завдання',
            'end_date': 'Коли закінчити задачу'
        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Назва завдання"}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Опишіть завдання'}),
            'perform': forms.Select(attrs={'class': 'form-control'}, choices=[('Я', 'Я')]),
            'status': forms.Select(attrs={'class': 'form-control'}, choices=[('В розробці', 'В розробці'), ('Виконано', 'Виконано')]),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class addMember(forms.ModelForm):
    class Meta:
        model = MembersProject
        fields = ['login_member', 'type']

        labels = {
            'login_member': "Логін учасника",
            'type': 'Яку роль виконує'
        }

        widgets = {
            'login_member': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ведіть логін учасника"}),
            'type': forms.Select(attrs={'class': 'form-control'}, choices=[('Адміністратор', 'Адміністратор'), ('Учасник', 'Учасник')])
        }
