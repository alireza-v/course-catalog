from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from .serializers import (
    UserProfileSer,
    ActivateMailSer,
    LoginSer,
    ResetRequestSer,
    ResetConfirmSer,
)

User = get_user_model()


class RegisterView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        operation_description="register user using email and password",
        request_body=UserProfileSer,
        responses={201: UserProfileSer},
    )
    def post(self, request):
        ser = UserProfileSer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(dict(message="Registration successful"), 201)
        return Response(ser.errors, 400)


class RequestMailActivation(APIView):
    @swagger_auto_schema(
        operation_description="request email activation",
    )
    def post(self, request):
        """DATA HARDCODED"""
        ser = ActivateMailSer(data=request.data)
        if ser.is_valid():
            user = User.objects.last()
            current_site = get_current_site(request)
            message2 = render_to_string(
                "accounts/email_confirmation.html",
                dict(
                    domain=current_site.domain,
                    uid=urlsafe_base64_encode(force_bytes(user.pk)),
                    token=PasswordResetTokenGenerator().make_token(user),
                ),
            )
            email = EmailMessage(
                "Email confirmation",
                message2,
                settings.EMAIL_HOST_USER,
                [user.email],
            )
            email.send()
            return Response(ser.data, 200)
        return Response(ser.errors, 400)


def activateMail(request, uidb64, token):
    """Activate user email"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myUser = User.objects.get(pk=uid)
    except User.DoesNotExist:
        myUser = None

    if myUser is not None and PasswordResetTokenGenerator().check_token(myUser, token):
        myUser.email_is_verified = True
        myUser.save()
        return JsonResponse(dict(message="Your account has been activated!"))
    else:
        return JsonResponse(dict(error="Failed to activate the account"))


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        operation_description="login using email and password",
        request_body=LoginSer,
    )
    def post(self, request):
        ser = LoginSer(data=request.data)
        if ser.is_valid():
            email = ser.validated_data["email"]
            password = ser.validated_data["password"]
            user = authenticate(request, email=email, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response(
                    dict(
                        refresh=str(refresh),
                        access=str(refresh.access_token),
                    ),
                    200,
                )
            else:
                return Response(
                    dict(
                        error="invalid email or password",
                    ),
                    400,
                )
        return Response(ser.errors, 400)


class ResetRequestView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        operation_description="reset password request",
        request_body=ResetRequestSer,
        responses={200: ResetRequestSer},
    )
    def post(self, request):
        ser = ResetRequestSer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(
                dict(
                    message="reset link has been sent",
                ),
                200,
            )
        return Response(ser.errors, 400)


class ResetConfirmView(View):
    template_name = "accounts/password_reset_confirm.html"

    def get(self, request, uidb64, token):
        return render(
            request,
            self.template_name,
            dict(
                form=None,
            ),
        )

    @swagger_auto_schema(
        operation_description="confirm password reset using password and password confirmation",
    )
    def post(self, request, uidb64, token):
        ser = ResetConfirmSer(
            data=dict(
                new_password=request.POST.get("new_password"),
                confirm_password=request.POST.get("confirm_password"),
                uid=uidb64,
                token=token,
            )
        )
        if ser.is_valid():
            ser.save()
            return JsonResponse(
                dict(
                    message="reset password success",
                )
            )
        return render(
            request,
            self.template_name,
            dict(
                form=None,
                error=ser.errors,
            ),
        )
