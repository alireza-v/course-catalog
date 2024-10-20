from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from rest_framework.test import APIClient
import pytest
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from faker import Faker

faker = Faker()
User = get_user_model()


@pytest.mark.django_db
class TestAccountsModel:
    """test suite for custom user model"""

    @pytest.fixture
    def user(db):
        """user creation fixture"""
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

    def testUserProfile(self, user):
        """test UserProfile using created credentials"""
        assert user.email
        assert user.check_password(user.raw_password)
        assert user.first_name
        assert user.last_name
        assert user.phone
        assert user.role == "student"


@pytest.mark.django_db
class TestAccountsView:
    """test suite for views including registration, login, email activation, reset password"""

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def user(db):
        """user creation fixture"""
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

    def testRegisteration(self, client):
        """registration test using email and password"""
        data = dict(
            email=faker.email(),
            password=faker.password(),
        )
        url = reverse("register")
        response = client.post(url, data)

        assert response.status_code == 201
        assert response.data["email"]

    def testActivateMail(self, client, user, mocker):
        """mail activation test"""
        mockedSendMail = mocker.patch.object(EmailMessage, "send", return_value=None)
        url = reverse("activateMail")
        response = client.post(url, data=dict(email=user.email))
        assert response.status_code == 200
        assert mockedSendMail.called
        assert mockedSendMail.call_count == 1

    def testActivateMailInvalidData(self, client):
        """test for invalid data sent to the email activation endpoint"""
        url = reverse("activateMail")
        response = client.post(url, data=dict())
        assert response.status_code == 400

    def testLogin(self, client, user):
        """test for login endpoint"""
        url = reverse("login")
        response = client.post(
            url,
            data=dict(
                email=user.email,
                password=user.raw_password,
            ),
        )
        assert response.status_code == 200
        assert "refresh" in response.data
        assert "access" in response.data

    def testResetRequest(self, client, user):
        """request for resetting password"""
        url = reverse("password_reset_request")
        data = dict(email=user.email)
        response = client.post(url, data)
        assert response.status_code == 200
        assert response.data["message"] == "reset link has been sent"

    @pytest.fixture
    def generateTokenUid(self, user):
        """generate valid uid and token for password resetting"""
        token = PasswordResetTokenGenerator().make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        return uid, token

    def testResetConfirm(self, client, generateTokenUid):
        """test rendering of resetting password"""
        uidb64, token = generateTokenUid
        url = reverse(
            "password_reset_confirm",
            kwargs=dict(
                uidb64=uidb64,
                token=token,
            ),
        )
        response = client.get(url)
        assert response.status_code == 200
