from django.db import models


class Projects(models.Model):
    title = models.CharField(max_length=255)
    logo = models.ImageField(null=True, blank=True, upload_to='logo_projects/', default='logo_projects/default_logo_projects.jpg')
    status = models.CharField(max_length=255, default='В розробці')
    deadline = models.DateTimeField()

    # project management
    access = models.TextField()
    author = models.CharField(max_length=15)

    # inviting url for project
    invite_url = models.TextField()


class RequestJoinProject(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    login_user = models.CharField(max_length=25)


class MembersProject(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    login_member = models.CharField(max_length=25)
    type = models.CharField(max_length=25, null=True)
    id_task = models.CharField(max_length=25, null=True)


class Tasks_Projects(models.Model):
    id_project = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    perform = models.TextField(null=True, default='All')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    status = models.CharField(max_length=30)


class ChatTeam(models.Model):
    id_project = models.IntegerField()


class MessagesChatTeam(models.Model):
    chat_id = models.IntegerField()
    login_author = models.CharField(max_length=15)

    message = models.TextField()
    time_message = models.DateTimeField(auto_now_add=True)