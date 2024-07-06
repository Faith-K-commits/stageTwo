from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

class RegisterEndpointTest(APITestCase):
    def test_register_successful(self):
        url = reverse('register')
        data = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "password": "password123",
            "phone": "0700000000"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_missing_fields(self):
        url = reverse('register')
        data = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_duplicate_email(self):
        url = reverse('register')
        data = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "password": "password123",
            "phone": "0700000000"
        }
        self.client.post(url, data, format='json')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)