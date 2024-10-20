from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from rest_framework import serializers
from .models import UserProfile


class UserProfileSer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ("email", "password")
        extra_kwargs = dict(
            password=dict(
                write_only=True,
            ),
        )

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = UserProfile.objects.create_user(
            email=validated_data["email"], password=password
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
            user = UserProfile.objects.get(email=value)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
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
        # email= self.validated_data["email"]
        # user= UserProfile.objects.get(email= email)
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
            self.user = UserProfile.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserProfile.DoesNotExist):
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
