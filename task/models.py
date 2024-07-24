from django.db import models
from fabricator.models import Fabricator
from project.models import Project
from django.conf import settings
from datetime import datetime
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
    task = models.ForeignKey('Task', on_delete=models.CASCADE, verbose_name='Task')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Commented By')
    created_on = models.DateTimeField(auto_now_add=True, verbose_name='Commented On')
    data = models.TextField(blank=True, verbose_name='Comment')
    file = models.FileField(upload_to=uploadCommentFile, null=True, verbose_name='Attachment', blank=True)
    objects = models.Manager()

class AssignedList(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE, verbose_name='Task')
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assigned_by', verbose_name='Assigned By')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assigned_to', verbose_name='Assigned To')
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='approved_by', verbose_name='Approved By', blank=True, null=True)
    approved_on = models.DateTimeField(verbose_name='Approved On', null=True, blank=True)
    assigned_on = models.DateTimeField(auto_now_add=True, verbose_name='Assigned On')
    approved = models.BooleanField(default=False, verbose_name='Approval Status')
    comment = models.TextField(blank=True, verbose_name='Comment on Approval', null=True)
    objects = models.Manager()

    def confirm(self, approved_by, comment=None):
        self.approved_by = approved_by
        self.approved_on = datetime.now()
        if comment:
            self.comment = comment
        self.approved = True
        self.save()
        # task = Task.objects.get(pk=self.task)
        self.task.user = self.assigned_to
        self.task.status = "ASSINGED"
        self.task.save()
        return self


class TaskPriority(models.IntegerChoices):
    LOW = 0, 'Low'
    NORMAL = 1, 'Normal'
    HIGH = 2, 'High'
    CRITICAL = 3, 'Critical'

class TaskManager(models.Manager):
    def create(self, assigned_by, **kwargs):
        project_obj = Project.objects.get(pk=kwargs['project'].id)
        
        kwargs['fabricator'] = project_obj.fabricator
        
        task = self.model(**kwargs)
        task.save()
        
        task.add_assignes(
            assigned_by=assigned_by,
            assigned_to=kwargs.get('user'),
            approved_by=assigned_by,
            approved_on=datetime.now(),
            approved=True,
            comment=None
        )
        
        return task  # Return the created task object

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Project')
    fabricator = models.ForeignKey(Fabricator, on_delete=models.CASCADE, verbose_name='Fabricator')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Parent Task')
    name = models.CharField(max_length=255, blank=False, verbose_name='Title')
    description = models.TextField(blank=True, verbose_name='Description')
    status = models.CharField(max_length=255, blank=False, verbose_name='Status', choices=[
        ('ASSINGED', 'Assigned'),
        ('IN-PROGRESS', 'In Progress'),
        ('ON-HOLD', 'On Hold'),
        ('BREAK', 'Break'),
        ('IN-REVIEW', 'In Review'),
        ('COMPLETE', 'Completed'),
        ('APPROVED', 'Approved')
    ], default='ASSIGNED')
    attachment = models.FileField(upload_to=uploadTaskFile, null=True, blank=True, verbose_name='Attachment')
    priority = models.IntegerField(blank=False, verbose_name='Priority', choices=TaskPriority.choices, default=TaskPriority.NORMAL)
    created_on = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(verbose_name='Due Date')
    duration = models.DurationField(verbose_name='Duration')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Current Assigne')

    objects = TaskManager()

    def get_child_tasks(self):
        return Task.objects.filter(parent=self)
    
    def get_assignes(self):
        return AssignedList.objects.filter(task=self)
    
    def add_assignes(self, **extra_kwargs):
        assignList = AssignedList.objects.create(
            task=self,
            assigned_by=extra_kwargs.get('assigned_by'),
            assigned_to=extra_kwargs.get('assigned_to'),
            approved_by=extra_kwargs.get('approved_by', None),
            approved_on=extra_kwargs.get('approved_on', None),
            approved=extra_kwargs.get('approved', False),
            comment=extra_kwargs.get('comment', None),
        )
        assignList.save()
        return assignList
    
    def update_assignes(self, id, **extra_kwargs):
        assignList = AssignedList.objects.get(id)
        assignList.assigned_by = extra_kwargs.get('assigned_by', assignList.assigned_by)
        assignList.assigned_to = extra_kwargs.get('assigned_to', assignList.assigned_to)
        assignList.approved_by = extra_kwargs.get('approved_by', assignList.approved_by)
        assignList.approved_on = datetime.now()
        assignList.approved = True
        assignList.comment = extra_kwargs.get('comment', assignList.comment)
        assignList.save()
        self.user = assignList.assigned_to
        self.save()
        return assignList
    
    def add_comment(self, user, data, file=None):
        comment = TaskComment.objects.create(
            task = self,
            user = user,
            data = data,
            file = file,
        )
        comment.save()
        return comment

    def get_comments(self):
        return TaskComment.objects.filter(task=self)

    def get_total_comments(self):
        return TaskComment.objects.filter(task=self).count()
