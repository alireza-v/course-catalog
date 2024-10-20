from django.urls import path
from .views import *

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("activeMail/", ActivateMailView.as_view(), name="activateMail"),
    path("activate/<uidb64>/<token>", activate, name="activate"),
    path("login/", LoginView.as_view(), name="login"),
    path("password-reset/", ResetRequestView.as_view(), name="password_reset_request"),
    path(
        "reset-password/<uidb64>/<token>/",
        ResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
]
