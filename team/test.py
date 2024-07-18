from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from team.models import Team, Member
from user.models import User

class TeamTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.team = Team.objects.create(name='Test Team')

    def test_get_team_members(self):
        url = reverse('team-members', kwargs={'pk': self.team.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_team_member(self):
        url = reverse('team-add-member', kwargs={'pk': self.team.pk})
        data = {
            'employee': self.user.pk,
            'role': 'Member'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_remove_team_member(self):
        member = Member.objects.create(team=self.team, employee=self.user, role='Member')
        url = reverse('team-remove-member', kwargs={'pk': self.team.pk, 'member_id': member.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_member_role(self):
        member = Member.objects.create(team=self.team, employee=self.user, role='Member')
        url = reverse('team-member-role', kwargs={'pk': self.team.pk, 'member_id': member.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)