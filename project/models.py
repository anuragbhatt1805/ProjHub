from django.db import models
from team.models import Team
from fabricator.models import Fabricator
from django.conf import settings
import os, uuid

def uploadFile(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'
    return os.path.join('project', filename)


class ProjectFile(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name='project')
    detail = models.CharField(max_length=255, blank=True, null=True)
    file = models.FileField(upload_to=uploadFile, null=True)
    objects = models.Manager()

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, blank=False, verbose_name='Project Name')
    description = models.TextField(blank=True, verbose_name='Project Description')
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='manager', verbose_name='Project Manager')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name='Team')
    fabricator = models.ForeignKey(Fabricator, on_delete=models.CASCADE, related_name='fabricator', verbose_name='Fabricator')
    startDate = models.DateTimeField(verbose_name='Start Date')
    endDate = models.DateTimeField(null=True, verbose_name='End Date')
    status = models.CharField(max_length=55, default='active', choices=[
        ('active', 'Active'),
        ('on-hold', 'On-Hold'),
        ('inactive', 'Inactive'),
        ('delayed', 'Delayed'),
        ('reopened', 'Reopened'),
        ('completed', 'Completed'),
        ('submitted', 'Submitted'),
        ('suspended', 'Suspended'),
        ('cancelled', 'Cancelled'),
    ], blank=True, null=True, verbose_name='Project Status')
    stage = models.CharField(max_length=55, default='IFA', choices=[
        ('IFA', 'Issue for Approval'),
        ('BFA', 'Back from Approval'),
        ('RIFA', 'Re-issue for Approval'),
        ('IFC', 'Issue for Construction'),
        ('BFC', 'Back from Construction'),
        ('RIFC', 'Re-issue for Construction'),
        ('RIF', 'Request for Information'),
        ('REV', 'Revision'),
    ], blank=True, null=True, verbose_name='Project Stage')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True  )
    objects = models.Manager()

    def get_all_files(self):
        return ProjectFile.objects.filter(project=self)
    
    def add_file(self, file, caption=None):
        file = ProjectFile.objects.create(
            project=self,
            detail=caption,
            file=file,
        )
        file.save()
        return file
    
    def get_file_count(self):
        return ProjectFile.objects.filter(project=self).count()

    def __str__(self):
        return self.name