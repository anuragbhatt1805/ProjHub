from django.db import models
from django.conf import settings
import uuid


class Member(models.Model):
    role = models.CharField(max_length=50, default='guest', verbose_name='Role')
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    objects = models.Manager()


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name='Team Name')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_by', verbose_name='Team Manager')
    members = models.ManyToManyField(Member, verbose_name='Team Members')
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='team_leader', verbose_name='Team Leader')
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()