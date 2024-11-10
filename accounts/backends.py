from django.contrib.auth.backends import ModelBackend

from accounts.models import CustomUser


class EmailBackend(ModelBackend):
    """Custom authentication backend using email and password"""

    def authenticate(self, request, email=None, password=None, **kwargs):
        user = self.get_user(email)
        if user and user.check_password(password):
            return user
        return None

    def get_user(self, email):
        try:
            return CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return None
