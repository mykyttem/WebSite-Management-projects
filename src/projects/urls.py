from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from . import main_funcs


urlpatterns = [    
    # main page
    path('', main_funcs.main_page, name='main-page'),

    # profile
    path('my-profile/<str:login>/create-project', main_funcs.create_project, name='create_project'),
    path('my-profile/<str:login>/projects', main_funcs.my_projects, name='projects'),
    
    # info for project
    path('project/<int:id>/<str:title>', views.project, name='project'),
    path('invite-member/project-<str:title>/author-project-<str:author>', views.inviteURL_member, name='invite-member'),
    path('project/<int:id>/<str:title>/list-requests-join', views.request_join, name='request-join'),
    path('project/<int:id>/<str:title>/project-settings', views.project_settings, name='project_settings'),
    path('project/<int:id>/<str:title>/tasks', views.tasks, name='tasks'),
    path('project/<int:id>/<str:title>/task/<int:id_task>/details', views.details_task, name='details_task'),
    path('project/<int:id>/<str:title>/team', views.team, name='team'),

    path('project/<int:id>/<str:title>/chat-team/<int:room_name>', views.chat_team, name='room'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)