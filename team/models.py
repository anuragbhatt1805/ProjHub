from typing import Any
from django.db import models
from django.conf import settings
import uuid


class Member(models.Model):
    team = models.ForeignKey('Team', on_delete=models.CASCADE, verbose_name='Team')
    role = models.CharField(max_length=50, default='GUEST', verbose_name='Role', choices=[
        ('GUEST', 'Guest'),
        ('LEADER', 'Leader'),
        ('MEMBER', 'Member'),
        ('MANAGER', 'Manager'),
        ('MODELER', 'Modeler'),
        ('CHECKER', 'Checker'),
        ('DETAILER', 'Detailer'),
        ('ERECTER', 'Erecter'),
        ('ADMIN', 'Admin')
    ])
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Employee')
    objects = models.Manager()

class TeamManager(models.Manager):

    def create(self, **kwargs):
        team = self.model(**kwargs)
        team.save()
        leadMember = Member.objects.create(
            team = team,
            role = 'LEADER',
            employee = team.leader
        )
        leadMember.save()
        return team


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name='Team Name')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_by', verbose_name='Team Manager', null=True, blank=True)
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='team_leader', verbose_name='Team Leader')
    created_at = models.DateTimeField(auto_now_add=True)
    objects = TeamManager()
    
    def get_members(self):
        return Member.objects.filter(team=self)
    
    def add_member(self, role, employee):
        member = Member.objects.create(
            team = self,
            role = role,
            employee = employee
        )
        member.save()
        return member
    
    def get_members_count(self):
        return self.get_members().count()
    
    def get_member_role(self, employee):
        return Member.objects.get(id=employee).role
    
    def remove_member(self, employee):
        member = Member.objects.get(id=employee)
        member.delete()
        return member