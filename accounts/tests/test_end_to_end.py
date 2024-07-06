from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class UserRegistrationTests(APITestCase):

    def setUp(self):
        self.url = reverse('accounts:register')  
        self.user_data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '1234567890',
            'password': 'password123'
        }

    def test_registration_success(self):
        response = self.client.post(self.url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data['data'])

    def test_registration_missing_fields(self):
        required_fields = ['firstName', 'lastName', 'email', 'password']
        for field in required_fields:
            invalid_data = self.user_data.copy()
            invalid_data.pop(field)
            response = self.client.post(self.url, invalid_data, format='json')
            self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_422_UNPROCESSABLE_ENTITY])
            self.assertIn(field, response.data['errors'])

    def test_registration_duplicate_email(self):
        self.client.post(self.url, self.user_data, format='json')
        response = self.client.post(self.url, self.user_data, format='json')
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_422_UNPROCESSABLE_ENTITY])
        self.assertIn('email', response.data['errors'])
