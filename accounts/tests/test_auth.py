import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from accounts.models import User, Organisation
from rest_framework_simplejwt.tokens import RefreshToken
import datetime

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user(db):
    def make_user(**kwargs):
        return User.objects.create_user(**kwargs)
    return make_user

@pytest.fixture
def get_or_create_organisation(db):
    def make_organisation(name="Default Organisation", **kwargs):
        organisation, _ = Organisation.objects.get_or_create(name=name, **kwargs)
        return organisation
    return make_organisation

@pytest.fixture
def user_token(create_user):
    user = create_user(email='test@example.com', password='password123', firstName='John', lastName='Doe')
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token), user

# Token Generation Test
def test_token_generation(user_token):
    token, user = user_token
    decoded_token = RefreshToken(token)
    assert decoded_token['user_id'] == user.id, "The token's user_id does not match the expected value"
    assert datetime.datetime.now() + datetime.timedelta(minutes=5) > decoded_token['exp'] > datetime.datetime.now(), "The token's expiry time is not within the expected range"

# Organisation Access Test
def test_organisation_access(api_client, create_user, get_or_create_organisation):
    user1 = create_user(email='user1@example.com', password='password123', firstName='User', lastName='One')
    user2 = create_user(email='user2@example.com', password='password123', firstName='User', lastName='Two')
    organisation = get_or_create_organisation()
    organisation.users.add(user1)
    api_client.force_authenticate(user=user2)
    response = api_client.get(reverse('add_user_to_organization', kwargs={'orgId': organisation.orgId}))
    assert response.status_code == status.HTTP_403_FORBIDDEN, "User2 should not have access to User1's organisation"

# End-to-End Test for Register Endpoint
@pytest.mark.django_db
def test_register_user_successfully(api_client):
    response = api_client.post(reverse('register'), data={
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'john@example.com',
        'password': 'password123',
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert 'John\'s Organisation' in response.data['data']['user']['organisations'], "The default organisation name is not correctly generated"
    assert 'accessToken' in response.data['data'], "Access token is missing in the response"

@pytest.mark.django_db
def test_login_user_successfully(api_client, create_user):
    user = create_user(email='login@example.com', password='password123', firstName='Login', lastName='User')
    response = api_client.post(reverse('login'), data={
        'email': 'login@example.com',
        'password': 'password123',
    })
    assert response.status_code == status.HTTP_200_OK
    assert 'accessToken' in response.data['data'], "Access token is missing in the response"

@pytest.mark.django_db
def test_register_user_missing_fields(api_client):
    required_fields = ['firstName', 'lastName', 'email', 'password']
    for field in required_fields:
        data = {f: 'test' for f in required_fields if f != field}
        response = api_client.post(reverse('register'), data=data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, f"Test failed for missing field: {field}"

@pytest.mark.django_db
def test_register_user_duplicate_email(api_client, create_user):
    create_user(email='duplicate@example.com', password='password123', firstName='Duplicate', lastName='User')
    response = api_client.post(reverse('register'), data={
        'firstName': 'Duplicate',
        'lastName': 'User',
        'email': 'duplicate@example.com',
        'password': 'password123',
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, "Duplicate email test failed"