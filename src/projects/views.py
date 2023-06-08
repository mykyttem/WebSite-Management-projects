from django.shortcuts import render, redirect

from datetime import datetime

from .models import Projects, MembersProject, Tasks_Projects
from .forms import CreateProjects, SettingsProject
from accounts.views import auth_user

#TODO: DELETE DUPCILATE CODE | Refactoring code
date_now = datetime.now()

@auth_user
def create_project(request, accounts_users, login):
    form = CreateProjects(request.POST)
  
    if request.method == 'POST':
        if form.is_valid():

            for user in accounts_users:  
                project = form.save(commit=False)
                project.author = user['login']

                form.save()

            return redirect('./projects')
  
    return render(request, 'create_project.html', {'form': form}) 


@auth_user
def projects(request, accounts_users, login):
    #TODO: add projects in which he also participates
    project_user = Projects.objects.filter(author=login).values()

    return render(request, 'projects.html', {'project_user': project_user}) 



@auth_user
def project(request, accounts_users, id, title):
    info_project = Projects.objects.filter(id=id).values()

    if not info_project:
        return render(request, 'not_found.html')


    for i in info_project:
        deadline = i['deadline'].replace(tzinfo=None)
        days_between_date = date_now - deadline

    return render(request, 'project.html', 
                {'accounts_users': accounts_users,
                    'title': title, 'id': id, 'info_project': info_project, 
                'date_now': date_now, 'days_between_date': abs(days_between_date.days)
    })


@auth_user
def project_settings(request, accounts_users, id, title):
    """
    Project settings
    Current data passing in file "forms" class - SettingsProject
    Update data for project
    """
    info_project = Projects.objects.filter(id=id).values()

    # if user not author project or not in list access 
    for user in accounts_users:
        login = user['login']
        for project in info_project:
            access = project['access']
            author = project['author']

            if login not in str(access).split() and not login == author:
                return redirect('/')
            

    # pass variable for forms
    form = SettingsProject(info_project=info_project)

    return render(request, 'project_settings.html', 
                {'id': id, 'title': title, 'form': form, 
                'date_now': date_now, 'info_project': info_project})


@auth_user
def tasks(request, accounts_users, id, title):
    info_project = Projects.objects.filter(id=id).values()
    tasks = Tasks_Projects.objects.filter(id_project=id).values()

    return render(request, 'tasks.html', 
                {'id': id, 'title': title, 'date_now': date_now, 
                'accounts_users': accounts_users, 'info_project': info_project,
                'tasks': tasks
    })


@auth_user
def info_task(request, accounts_users, id, title):
    info_project = Projects.objects.filter(id=id).values()

    return render(request, 'tasks.html', 
                {'id': id, 'title': title, 'date_now': date_now, 
                'accounts_users': accounts_users, 'info_project': info_project
    })


@auth_user
def team(request, accounts_users, id, title):
    info_project = Projects.objects.filter(id=id).values()
    members = MembersProject.objects.filter(id_project=id).values()


    return render(request, 'team.html', 
                {'id': id, 'title': title, 'date_now': date_now, 
                'accounts_users': accounts_users, 'info_project': info_project,
                'members': members
    })