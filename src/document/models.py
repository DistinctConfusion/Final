from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from django.db.models.signals import post_save
from django.dispatch import receiver

from account.models import Account

# Create your models here.

class Project(models.Model):
    proj_id = models.BigAutoField(primary_key=True)
    #Previous iteration. After a project has been confirmed by 2 parties, any changes are logged
    prev_iter = models.IntegerField(null=True)
    proj_name = models.CharField(max_length=50)
    deleted = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=False)

class ProjectAccount(models.Model):
    project_id = models.IntegerField(null=False,blank=False)
    collaborator = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    user_confirm = models.BooleanField(default=False)

class Specification(models.Model):
    spec_id = models.BigAutoField(primary_key=True)
    related_proj = models.ForeignKey(Project, on_delete=models.CASCADE)
    prev_iter = models.IntegerField(null=True)
    spec_name = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    deleted = models.BooleanField(default=False)


class Changelog(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    action = models.TextField(null=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)