from django.shortcuts import render, redirect

from datetime import datetime

from .models import Projects, MembersProject, Tasks_Projects, MembersProject, MessagesChatTeam
from .forms import CreateProjects, SettingsProject, TaskProjects, addMember
from accounts.views import auth_user

date_now = datetime.now()

#TODO: REFACTORING | DELETE GLOBALS VARIABLE, ADDED CLASSES
info_project = None
tasks_value = None
days_between_date = None

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


#TODO: Invite for project, delete from project, other
@auth_user
def project(request, accounts_users, id, title):
    global info_project
    global tasks_value
    global days_between_date

    info_project = Projects.objects.filter(id=id).values()
    tasks_value = Tasks_Projects.objects.filter(id_project=id).values()

    if not info_project:
        return render(request, 'not_found.html')


    for i in info_project:
        deadline = i['deadline'].replace(tzinfo=None)
        days_between_date = date_now - deadline
        days_between_date = abs(days_between_date.days)


    return render(request, 'project.html', 
                {'accounts_users': accounts_users, 'tasks': tasks_value,
                'title': title, 'id': id, 'info_project': info_project, 
                'date_now': date_now, 'days_between_date': days_between_date,
    })


@auth_user
def project_settings(request, accounts_users, id, title):
    """
    Project settings
    Current data passing in file "forms" class - SettingsProject
    Update data for project
    """

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

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(f'/project/{id}/{title}')


    return render(request, 'project_settings.html', 
                {'id': id, 'title': title, 'form': form, 
                'date_now': date_now, 'info_project': info_project,
                'tasks': tasks_value, 'days_between_date': days_between_date})


@auth_user
def tasks(request, accounts_users, id, title):
    """  
    Create task
    List tasks
    Delete
    """
    form = TaskProjects(request.POST)

    # delete taks button
    if 'id_task_delete' in request.GET:
        id_task_delete = request.GET.get('id_task_delete')
        Tasks_Projects.objects.filter(id=id_task_delete).delete()

        return redirect(f'/project/{id}/{title}')


    # create task
    if request.method == 'POST':
        if form.is_valid():
            task = form.save(commit=False)
            task.id_project = id

            form.save()

            return redirect(f'/project/{id}/{title}')


    return render(request, 'tasks.html', 
                {'id': id, 'title': title, 
                'date_now': date_now, 'accounts_users': accounts_users,
                'info_project': info_project, 'tasks': tasks_value,
                'form': form, 'days_between_date': days_between_date
    })


@auth_user
def details_task(request, accounts_users, id, title, id_task):
    d_task = Tasks_Projects.objects.filter(id=id_task).values()    


    return render(request, 'details_task.html', 
                {'id': id, 'title': title, 'date_now': date_now, 
                'accounts_users': accounts_users, 'info_project': info_project,
                'tasks': tasks_value, 'days_between_date': days_between_date,
                'd_task': d_task
    })


@auth_user
def team(request, accounts_users, id, title):
    members = MembersProject.objects.filter(id_project=id).values()
    form = addMember(request.POST)

    # delete member button
    if 'id_member_delete' in request.GET:
        id_member_delete = request.GET.get('id_member_delete')
        MembersProject.objects.filter(id=id_member_delete).delete()

        return redirect(f'/project/{id}/{title}')

    # add member
    if request.method == 'POST':
        if form.is_valid():
            member = form.save(commit=False)
            member.id_project = id

            form.save()

            return redirect(f'/project/{id}/{title}')    


    return render(request, 'team.html', 
                {'id': id, 'title': title, 'date_now': date_now, 
                'accounts_users': accounts_users, 'info_project': info_project,
                'members': members, 'tasks': tasks_value, 'days_between_date': days_between_date,
                'form': form
    })


#TODO: read and write chat, only members project, more options
#FIXME: HTML - reverse
@auth_user
def chat_team(request, accounts_users, id, title, room_name):
    user_login = request.session.get('user-login')

    messages = MessagesChatTeam.objects.filter(chat_id=id).values()


    return render(request, 'chat_team.html', {
        "room_name": room_name, 'user_login': user_login,
        'messages': messages
    })