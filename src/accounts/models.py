from django.db import models


class Accounts(models.Model):
    name = models.CharField(max_length=15)
    login = models.CharField(max_length=15)
    email = models.EmailField(max_length=255)
    avatar = models.ImageField(null=True, blank=True, upload_to='avatars/', default='avatars/default_avatar.jpeg')

    password = models.CharField(max_length=500)


class Projects(models.Model):
    title = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    team_members = models.TextField(null=True)
    status = models.CharField(max_length=255, default='В розробці')

    # project management
    access = models.TextField()
    author = models.CharField(max_length=15)


class Tasks_Projects(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    perform = models.TextField(null=True, default='All')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()