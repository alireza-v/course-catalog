from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from .managers import UserProfileManager


class BaseModel(models.Model):
    """Abstract base model which includes timestamp and updated fields"""

    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserProfile(AbstractUser, BaseModel):
    """Custom user model for handling profiles with email-based authentication"""

    class Roll(models.TextChoices):
        STUDENT = "student", "Student"
        MENTOR = "mentor", "Mentor"

    username = None
    email = models.EmailField(unique=True)
    email_is_verified = models.BooleanField(default=False, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = PhoneNumberField()
    role = models.CharField(max_length=10, choices=Roll.choices, default=Roll.STUDENT)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserProfileManager()

    class Meta:
        ordering = ("-timestamp",)

    def __str__(self):
        return self.email
