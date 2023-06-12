from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [    
    path('my-profile/<str:login>/create-project', views.create_project, name='create_project'),
    path('my-profile/<str:login>/projects', views.projects, name='projects'),
    
    path('project/<int:id>/<str:title>', views.project, name='project'),
    path('project/<int:id>/<str:title>/project-settings', views.project_settings, name='project_settings'),
    path('project/<int:id>/<str:title>/tasks', views.tasks, name='tasks'),
    path('project/<int:id>/<str:title>/task/<int:id_task>/details', views.details_task, name='details_task'),
    path('project/<int:id>/<str:title>/team', views.team, name='team'),

    path('project/<int:id>/<str:title>/chat-team/<int:room_name>', views.chat_team, name='room'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)