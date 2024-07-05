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
    detail = models.CharField(max_length=255)
    file = models.FileField(upload_to=uploadFile, null=True)

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='manager')
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    fabricator = models.ForeignKey(Fabricator, on_delete=models.CASCADE, related_name='fabricator')
    startDate = models.DateTimeField()
    endDate = models.DateTimeField(null=True)
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
    ])
    stage = models.CharField(max_length=55, default='IFA', choices=[
        ('IFA', 'Issue for Approval'),
        ('BFA', 'Back from Approval'),
        ('RIFA', 'Re-issue for Approval'),
        ('IFC', 'Issue for Construction'),
        ('BFC', 'Back from Construction'),
        ('RIFC', 'Re-issue for Construction'),
        ('RIF', 'Request for Information'),
        ('REV', 'Revision'),
    ])
    files = models.ManyToManyField(ProjectFile, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()