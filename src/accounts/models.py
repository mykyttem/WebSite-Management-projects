from django.db import models


class Accounts(models.Model):
    name = models.CharField(max_length=15)
    login = models.CharField(max_length=15)
    email = models.EmailField(max_length=255)
    avatar = models.ImageField(null=True, blank=True, upload_to='avatars/', default='avatars/default_avatar.jpeg')

    password = models.CharField(max_length=500)