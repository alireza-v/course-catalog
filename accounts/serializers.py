from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers

from .models import *

User = get_user_model()


class CustomUserSer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ("email", "password", "role", "is_superuser")
        extra_kwargs = dict(
            password=dict(
                write_only=True,
            ),
        )

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(
            email=validated_data.get("email"),
            password=password,
            role=validated_data.get("role"),
        )
        if password:
            user.set_password(password)
            user.save()
        return user


class ActivateMailSer(serializers.Serializer):
    email = serializers.EmailField()


class LoginSer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class ResetRequestSer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "This email address is not associated with any account"
            )
        self.context["user"] = user
        return value

    def send_password_reset_email(self, user):
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user=user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"{settings.BACKEND_URL}/reset-password/{uid}/{token}/"
        html_message = render_to_string(
            "accounts/password_reset_email.html",
            dict(
                user=user,
                reset_link=reset_link,
            ),
        )
        plain_message = strip_tags(html_message)
        send_mail(
            subject="password reset request",
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            html_message=html_message,
        )

    def save(self):
        user = self.context["user"]
        self.send_password_reset_email(user)


class ResetConfirmSer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match.")
        try:
            uid = urlsafe_base64_decode(data["uid"]).decode()
            self.user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("invalid user id")
        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(self.user, data["token"]):
            raise serializers.ValidationError("invalid or expired token")
        return data

    def save(self):
        password = self.validated_data["new_password"]
        self.user.set_password(password)
        self.user.save()
        return self.user
