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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Commented By')
    created_on = models.DateTimeField(auto_now_add=True, verbose_name='Commented On')
    data = models.TextField(blank=True, verbose_name='Comment')
    file = models.FileField(upload_to=uploadCommentFile, null=True, verbose_name='Attachment')
    objects = models.Manager()

class AssignedList(models.Model):
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assigned_by', verbose_name='Assigned By')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assigned_to', verbose_name='Assigned To')
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='approved_by', verbose_name='Approved By')
    approved_on = models.DateTimeField(auto_now=True, verbose_name='Approved On')
    assigned_on = models.DateTimeField(auto_now_add=True, verbose_name='Assigned On')
    approved = models.BooleanField(default=False, verbose_name='Approval Status')
    comment = models.TextField(blank=True, verbose_name='Comment on Approval')
    objects = models.Manager()

class TaskPriority(models.IntegerChoices):
    LOW = 0, 'Low'
    NORMAL = 1, 'Normal'
    HIGH = 2, 'High'
    CRITICAL = 3, 'Critical'

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Project')
    fabricator = models.ForeignKey(Fabricator, on_delete=models.CASCADE, verbose_name='Fabricator')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Parent Task')
    name = models.CharField(max_length=255, blank=False, verbose_name='Title')
    description = models.TextField(blank=True, verbose_name='Description')
    status = models.CharField(max_length=255, blank=False, verbose_name='Status', choices=[
        ('ASSINGED', 'Assigned'),
        ('ON-HOLD', 'On-Hold'),
        ('BREAK', 'Break'),
        ('APPROVED', 'Approved'),
        ('COMPLETE', 'Completed')
    ], default='ASSIGNED')
    attachment = models.FileField(upload_to=uploadTaskFile, null=True, blank=True, verbose_name='Attachment')
    priority = models.IntegerField(blank=False, verbose_name='Priority', choices=TaskPriority.choices, default=TaskPriority.NORMAL)
    created_on = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(verbose_name='Due Date')
    duration = models.DurationField(verbose_name='Duration')
    comments = models.ManyToManyField(TaskComment, blank=True, verbose_name='Comments')
    assignes = models.ManyToManyField(AssignedList, blank=True, verbose_name='Assign List')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Current Assigne')

    objects = models.Manager()

    def get_child_tasks(self):
        return Task.objects.filter(parent=self)
