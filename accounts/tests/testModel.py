import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from faker import Faker
from rest_framework.test import APIClient

faker = Faker()
User = get_user_model()


@pytest.fixture
def user(db):
    """User creation fixture"""
    raw_password = "123!@#QWE"
    user = User.objects.create_user(
        email=faker.email(),
        password=raw_password,
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        phone=faker.phone_number(),
        role="student",
    )
    user.raw_password = raw_password
    return user


@pytest.mark.django_db
class TestAccountsModel:
    """test suite for custom user model"""

    def testUserProfile(self, user):
        """Test UserProfile using created credentials"""
        assert user.email
        assert user.check_password(user.raw_password)
        assert user.first_name
        assert user.last_name
        assert user.phone
        assert user.role == "student"
