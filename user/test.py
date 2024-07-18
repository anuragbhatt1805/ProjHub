from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from user.models import User, PushRecord, TaskRecord
from user.serializers import UserSerializer, PunchRecordSerializer, TaskRecordSerializer, TaskRecordDetailSerializer

class UserViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.client.force_authenticate(user=self.user)

    def test_me_view(self):
        url = reverse('user-me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, UserSerializer(self.user).data)

class PunchRecordViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.client.force_authenticate(user=self.user)
        self.punch_record = PushRecord.objects.create(user=self.user)

    def test_start_view(self):
        url = reverse('punchrecord-start', args=[self.punch_record.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user'], self.user.id)
        self.assertEqual(response.data['punch_type'], 'start')

    def test_end_view(self):
        url = reverse('punchrecord-end', args=[self.punch_record.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user'], self.user.id)
        self.assertEqual(response.data['punch_type'], 'end')

    # Add more test methods for other views...

class TaskRecordViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.client.force_authenticate(user=self.user)
        self.task_record = TaskRecord.objects.create(user=self.user, task='Test Task')

    def test_retrieve_view(self):
        url = reverse('taskrecord-detail', args=[self.task_record.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, TaskRecordDetailSerializer(self.task_record).data)

    # Add more test methods for other views...
