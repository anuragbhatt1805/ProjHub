from django.db import models
from fabricator.models import Fabricator
from project.models import Project
from django.conf import settings
import os, uuid

def uploadTaskFile(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'
    return os.path.join('task', filename)

def uploadCommentFile(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'
    return os.path.join('comment', filename)

class TaskComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    data = models.TextField(blank=True)
    file = models.FileField(upload_to=uploadCommentFile, null=True)
    objects = models.Manager()

class AssignedList(models.Model):
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assigned_by')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assigned_to')
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='approved_by')
    approved_on = models.DateTimeField(auto_now=True)
    assigned_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    comment = models.TextField(blank=True)
    objects = models.Manager()


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    fabricator = models.ForeignKey(Fabricator, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    child = models.ManyToManyField('self', blank=True)
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=255, blank=False)
    priority = models.IntegerField(blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    duration = models.DurationField()
    comments = models.ManyToManyField(TaskComment, blank=True)
    assignes = models.ManyToManyField(AssignedList, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    objects = models.Manager()
