from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q

from .models import Projects, MembersProject, Tasks_Projects, RequestJoinProject
from .forms import CreateProjects
from accounts.views import auth_user


# main page
def main_page(request):
    user_login = request.session.get('user-login')  
    all_projects = Projects.objects.all()

    if 'send-request-join-project' in request.POST:
        id_project_send = request.POST['send-request-join-project']
        project = Projects.objects.filter(id=id_project_send).first()


        if RequestJoinProject.objects.filter(login_user=user_login).exists():
            messages.success(request, 'Ви вже брали участь')
            return redirect('./')    
        else:

            save_request = RequestJoinProject(project=project, login_user=user_login)
            save_request.save()

            return redirect('./')    
    
    return render(request, 'main_page.html', {'user_login': user_login, 'all_projects': all_projects})


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
        members = MembersProject.objects.filter(project_id=id).values()

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


@auth_user
def create_project(request, accounts_users):
    login = request.session.get('user-login')
    form = CreateProjects(request.POST, request.FILES)
  
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


@auth_user
def my_projects(request, accounts_users):
    """ Geting projects, member in projects or author project """
    login = request.session.get('user-login')

    members_projects = MembersProject.objects.filter(login_member=login).values('project_id')
    project_user = Projects.objects.filter(Q(author=login) or Q(id__contains=members_projects)).values()

    return render(request, 'my_projects.html', {'project_user': project_user, 'members_projects': members_projects}) 