from django import forms
from .models import Projects, Tasks_Projects

class CreateProjects(forms.ModelForm):
    class Meta:
   
        model = Projects
        fields = ['title', 'deadline', 'team_members', 'access']

        labels = {
            'title': "Назва проекту",
            'team_members': 'Учасники',
            'access': 'Хто має доступ керування проектом',
            'deadline': 'Крайний термін'
        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ведіть назву проекту"}),
            'deadline': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}),
            'team_members': forms.Select(attrs={'class': 'form-control'}, choices=[('Я', 'Я')]),
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
        fields = ['title', 'deadline', 'team_members', 'access', 'status']

        labels = {
            'title': "Назва проекту",
            'team_members': 'Учасники',
            'status': 'Статус',
            'access': 'Хто має доступ керування проектом',
            'deadline': 'Крайний термін'
        }
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Змінити назву проекту"}),
            'deadline': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}),
            'team_members': forms.Select(attrs={'class': 'form-control'}, choices=[('Я', 'Я')]),
            'status': forms.Select(attrs={'class': 'form-control'}, choices=[('В розробці', 'В розробці'), ('Завершено', 'Завершено')]),
            'access': forms.Select(attrs={'class': 'form-control'}, choices=[('Я', 'Я')])
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