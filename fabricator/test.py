from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from fabricator.models import Fabricator

class FabricatorModelViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.fabricator = Fabricator.objects.create(name='Test Fabricator', contactPerson='John Doe', contactCountry='USA', contactState='California', contactCity='Los Angeles')

    def test_list_fabricators(self):
        response = self.client.get('/fabricators/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Fabricator')

    def test_create_fabricator(self):
        data = {
            'name': 'New Fabricator',
            'contactPerson': 'Jane Smith',
            'contactCountry': 'Canada',
            'contactState': 'Ontario',
            'contactCity': 'Toronto'
        }
        response = self.client.post('/fabricators/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Fabricator.objects.count(), 2)
        self.assertEqual(Fabricator.objects.last().name, 'New Fabricator')

    def test_update_fabricator(self):
        data = {
            'name': 'Updated Fabricator',
            'contactPerson': 'John Doe',
            'contactCountry': 'USA',
            'contactState': 'California',
            'contactCity': 'San Francisco'
        }
        response = self.client.put(f'/fabricators/{self.fabricator.id}/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Fabricator.objects.get(id=self.fabricator.id).contactCity, 'San Francisco')

    def test_delete_fabricator(self):
        response = self.client.delete(f'/fabricators/{self.fabricator.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Fabricator.objects.count(), 0)