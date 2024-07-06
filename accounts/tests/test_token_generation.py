from datetime import datetime, timedelta
from rest_framework_simplejwt.tokens import RefreshToken
from django.test import TestCase
from django.utils import timezone
from accounts.models import User, Organisation
from rest_framework.test import APIClient
from rest_framework import status

class TokenGenerationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='password')

    def test_token_generation(self):
        refresh = RefreshToken.for_user(self.user)
        self.assertIsInstance(refresh, RefreshToken)
        self.assertTrue(refresh.access_token)

    def test_token_expiration(self):
        refresh = RefreshToken.for_user(self.user)
        token_lifetime = refresh.access_token.lifetime.total_seconds()
        expiration_time = timezone.now() + timedelta(seconds=token_lifetime)
        self.assertLessEqual(expiration_time, timezone.now() + timedelta(seconds=token_lifetime + 5))
        self.assertGreaterEqual(expiration_time, timezone.now() + timedelta(seconds=token_lifetime - 5))