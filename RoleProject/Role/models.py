from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Role(models.Model):
    name = models.CharField(max_length=200, unique=True)
    status_id = models.ForeignKey('Status', on_delete=models.CASCADE)
    create_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_roles')
    approve_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approved_roles')
    user = models.ManyToManyField(User, through='UserRole')
    servers = models.ManyToManyField('Server', through='ServersForRole')


class ServersForRole(models.Model):
    server_id = models.ForeignKey('Server', on_delete=models.CASCADE)
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE)


class UserRole(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE)
    server_id = models.ForeignKey('Server', on_delete=models.CASCADE)


class Server(models.Model):
    server_name = models.CharField(max_length=300, unique=True)


class Status(models.Model):
    status = models.CharField(max_length=100, unique=True)


class Right(models.Model):
    name = models.CharField(max_length=200, unique=True)
    type_id = models.ForeignKey('RightType', on_delete=models.CASCADE)
    command = models.CharField(max_length=300)
    check_right = models.CharField(max_length=300)
    role = models.ManyToManyField('Role')


class RightType(models.Model):
    type = models.CharField(max_length=100, unique=True)