from django.db import models


class Projects(models.Model):
    title = models.CharField(max_length=255)
    team_members = models.TextField(null=True)
    status = models.CharField(max_length=255, default='В розробці')
    deadline = models.DateTimeField()

    # project management
    access = models.TextField()
    author = models.CharField(max_length=15)


class Tasks_Projects(models.Model):
    id_project = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    perform = models.TextField(null=True, default='All')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    status = models.CharField(max_length=30)


class MembersProject(models.Model):
    id_project = models.IntegerField()
    login_member = models.CharField(max_length=25)
    type = models.CharField(max_length=25)
    id_task = models.CharField(max_length=25)