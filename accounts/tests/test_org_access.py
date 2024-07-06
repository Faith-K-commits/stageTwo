from django.test import TestCase
from accounts.models import User, Organisation
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.test import APITestCase

class OrganisationAccessTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='test@example.com', password='password', firstName='John', lastName='Doe')
        self.client.force_authenticate(user=self.user)
        
        # Create an organization and associate it with the user
        self.org = Organisation.objects.create(orgId='org123', name='Test Org')
        # Assuming there is a many-to-many relationship between User and Organisation
        self.org.users.add(self.user)
        self.org.save()

    def test_get_organisations(self):
        response = self.client.get('/api/organisations/')
        print(response.data)  # Debugging statement
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Test Org', [org['name'] for org in response.data['data']['organisations']])

    def test_get_organisation(self):
        response = self.client.get(f'/api/organisations/{self.org.orgId}/')  # Use correct URL with organization ID
        print(response.data)  # Debugging statement
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Org')