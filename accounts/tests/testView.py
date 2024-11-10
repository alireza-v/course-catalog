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


@pytest.mark.django_db
class TestAccountsView:
    """test suite for views including registration, login, email activation, reset password"""

    @pytest.fixture
    def client(self):
        return APIClient()

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

    def testRegisteration(self, client):
        """Registration test using email and password"""
        data = dict(email=faker.email(), password=faker.password(), role="student")
        url = reverse("register")
        response = client.post(url, data)

        assert response.status_code == 201
        # assert response.data["email"]

    def testActivateMail(self, client, user, mocker):
        """Mail activation test"""
        mockedSendMail = mocker.patch.object(EmailMessage, "send", return_value=None)
        url = reverse("request-mail-acc")
        response = client.post(url, data=dict(email=user.email))
        assert response.status_code == 200
        assert mockedSendMail.called
        assert mockedSendMail.call_count == 1

    def testActivateMailInvalidData(self, client):
        """Test for invalid data sent to the email activation endpoint"""
        url = reverse("request-mail-acc")
        response = client.post(url, data=dict())
        assert response.status_code == 400

    def testLogin(self, client, user):
        """Test for login endpoint"""
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
        """Request for resetting password"""
        url = reverse("password-reset-request")
        data = dict(email=user.email)
        response = client.post(url, data)
        assert response.status_code == 200
        assert response.data["message"] == "Reset link has been sent"

    @pytest.fixture
    def generateTokenUid(self, user):
        """Generate valid uid and token for password resetting"""
        token = PasswordResetTokenGenerator().make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        return uid, token

    def testResetConfirm(self, client, generateTokenUid):
        """Test rendering of resetting password"""
        uidb64, token = generateTokenUid
        url = reverse(
            "password-reset-confirm",
            kwargs=dict(
                uidb64=uidb64,
                token=token,
            ),
        )
        response = client.get(url)
        assert response.status_code == 200
