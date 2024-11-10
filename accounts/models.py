from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .managers import *


class BaseModel(models.Model):
    """Abstract base model which includes timestamp and updated fields"""

    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Role(models.TextChoices):
    STUDENT = "student", "Student"
    MENTOR = "mentor", "Mentor"


class CustomUser(AbstractUser, BaseModel):
    """Custom user model for handling profiles with email-based authentication"""

    username = None
    email = models.EmailField(unique=True)
    email_is_verified = models.BooleanField(default=False, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = PhoneNumberField()
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
