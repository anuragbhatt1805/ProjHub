from django.db import models
from django.conf import settings
import uuid


class Member(models.Model):
    role = models.CharField(max_length=50, default='guest')
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    objects = models.Manager()


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_by')
    members = models.ManyToManyField(Member)
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='team_leader')
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()