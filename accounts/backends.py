from django.contrib.auth.backends import ModelBackend

from accounts.models import UserProfile


class EmailBackend(ModelBackend):
    """custom authentication and that is based on email and password"""

    def authenticate(self, request, email=None, password=None, **kwargs):
        user = self.get_user(email)
        if user and user.check_password(password):
            return user
        return None

    def get_user(self, email):
        try:
            return UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            return None
