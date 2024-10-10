from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from .managers import *


class UserProfile(AbstractUser):

    class Roll(models.TextChoices):
        STUDENT="student", "Student"
        MENTOR="mentor", "Mentor"

    username=None
    email=models.EmailField(unique=True)
    first_name=models.CharField(max_length=10)
    last_name=models.CharField(max_length=10)
    phone=models.CharField(max_length=20)
    role=models.CharField(max_length=10, choices=Roll.choices)

    # is_staff=models.BooleanField(default=True)
    # is_superuser=models.BooleanField(default=True)
    # is_active=models.BooleanField(default=True)

    timestamp=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    USERNAME_FIELD="email"
    REQUIRED_FIELDS=["first_name", "last_name"]

    objects=UserProfileManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        # if self.role==self.Roll.MENTOR:
        #     return True
        return True

    def has_module_perms(self, app_label):
        return True



