from django.urls import path
from .views import *

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("request-mail-acc/", RequestMailActivation.as_view(), name="request-mail-acc"),
    path("activate/<uidb64>/<token>", activateMail, name="activate"),
    path("login/", LoginView.as_view(), name="login"),
    path(
        "password-reset-request/",
        ResetRequestView.as_view(),
        name="password-reset-request",
    ),
    path(
        "reset-password/<uidb64>/<token>/",
        ResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
]
