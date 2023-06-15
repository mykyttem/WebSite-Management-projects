from django.shortcuts import render, redirect
from django.db.models import Q

from datetime import datetime

from .models import Projects, MembersProject, Tasks_Projects, MessagesChatTeam
from .forms import CreateProjects, SettingsProject, TaskProjects, addMember
from accounts.views import auth_user


# decorator checking user members in project ot author
def checkMember_project(f):
    """
    Using decorator "auth_user", get accounts users
    Checking member in project or author
    When we use the "checkingUser_project" decorator, 
    we simultaneously check the user's authorization and participation in the project,
    whether he is the author of the project
    """

    @auth_user
    def checkingUser_project(request, accounts_users, id, *args, **kwargs):
 
        # info for project
        info_project = Projects.objects.filter(id=id).values()
        tasks_value = Tasks_Projects.objects.filter(id_project=id).values()
        members = MembersProject.objects.filter(id_project=id).values()

        # checking user in project members
        for user in accounts_users:
            login_user = user['login']

            # checking if author project
            if not Projects.objects.filter(id=id, author=login_user).values():
                
                # checking if user member for project
                members_project = MembersProject.objects.filter(login_member=login_user).exists()

                if not members_project:
                    return redirect(f'/my-profile/{login_user}')
                

            return f(request, accounts_users, id, info_project, tasks_value, members, *args, **kwargs)
    return checkingUser_project
        

date_now = datetime.now()
days_between_date = None

#FIXME URLS For login
#FIXME: save my logo
@auth_user
def create_project(request, accounts_users, login):
    form = CreateProjects(request.POST)
  
    if request.method == 'POST':
        if form.is_valid():
            # get input user
            input_fields = form.cleaned_data
            i_title = input_fields['title']

            # save
            project = form.save(commit=False)
            project.author = login
            project.invite_url = f"/invite-member/project-{i_title}/author-project-{login}"

            form.save()

        return redirect('./projects')

    return render(request, 'create_project.html', {'form': form}) 


#FIXME URLS For login
@auth_user
def projects(request, accounts_users, login):
    """ Geting projects, member in projects or author project """

    members_projects = MembersProject.objects.filter(login_member=login).values('id_project')
    project_user = Projects.objects.filter(Q(author=login) or Q(id__contains=members_projects)).values()

    return render(request, 'projects.html', {'project_user': project_user, 'members_projects': members_projects}) 


@checkMember_project
def project(request, accounts_users, id, info_project, tasks_value, members, title):
    global days_between_date


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
                'members': members
    })


@auth_user
def inviteURL_member(request, accounts_users, title, author):
    project = Projects.objects.filter(title=title, author=author).values()

    for p in project:
        url_project = redirect (f"/project/{p['id']}/{title}")

        # add member in list members for project
        for user in accounts_users:
           save_member = MembersProject(id_project=p['id'], login_member=user['login'], type=None, id_task=None)
           save_member.save()

           return url_project
        

@checkMember_project
def project_settings(request, accounts_users, id, info_project, tasks_value, members, title):
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
                {
                    'id': id, 'title': title, 'form': form, 
                    'date_now': date_now, 'info_project': info_project,
                    'tasks': tasks_value, 'days_between_date': days_between_date,
                    'members': members
                })


@checkMember_project
def tasks(request, accounts_users, id, info_project, tasks_value, members, title):
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
                'form': form, 'days_between_date': days_between_date,
                'members': members
    })


@checkMember_project
def details_task(request, accounts_users, id, title, info_project, tasks_value, members, id_task):
    d_task = Tasks_Projects.objects.filter(id=id_task).values()    


    return render(request, 'details_task.html', 
                {'id': id, 'title': title, 'date_now': date_now, 
                'accounts_users': accounts_users, 'info_project': info_project,
                'tasks': tasks_value, 'days_between_date': days_between_date,
                'd_task': d_task, 'members': members
    })


@checkMember_project
def team(request, accounts_users, id, info_project, tasks_value, members, title):
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


@checkMember_project
def chat_team(request, accounts_users, id, info_project, tasks_value, members, title, room_name):
    response = redirect(f'./{id}')
    
    user_login = request.session.get('user-login')
    messages = MessagesChatTeam.objects.filter(chat_id=id).values()

    # btn del msg
    if 'id_msg_click_del' in request.GET:
        id_msg_click = request.GET.get('id_msg_click_del')
        msg_del = MessagesChatTeam.objects.get(id=id_msg_click)
        msg_del.delete()

        return response

    # btn edit msg
    if 'editMsgInput' in request.GET:
        id_msg_click_edit = request.GET.get('id_msg_click_edit')
        msg_edit = MessagesChatTeam.objects.get(id=id_msg_click_edit)

        editMsgInput = request.GET.get('editMsgInput')
        
        if msg_edit:
            msg_edit.message = editMsgInput
            msg_edit.save()
            return response


    return render(request, 'chat_team.html', {
        'accounts_users': accounts_users,
        "room_name": room_name, 'user_login': user_login,
        'messages': messages, 'info_project': info_project, 'title': title,
        'members': members
    })